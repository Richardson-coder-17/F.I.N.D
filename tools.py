import pandas as pd
import networkx as nx
from crewai.tools import tool
from pyvis.network import Network

def build_fraud_graph(csv_source):
    if isinstance(csv_source, str) or hasattr(csv_source, 'read'):
        df = pd.read_csv(csv_source)
    else:
        df = csv_source.copy()

    df.columns = df.columns.str.strip().str.lower()

    column_mapping = {
        'source': 'sender', 'from': 'sender', 'sender_account': 'sender', 'sender_id': 'sender', 'origin': 'sender',
        'target': 'receiver', 'to': 'receiver', 'receiver_account': 'receiver', 'receiver_id': 'receiver', 'destination': 'receiver',
        'ip_address': 'ip', 'device': 'device_id'
    }
    df = df.rename(columns=column_mapping)

    if 'sender' not in df.columns or 'receiver' not in df.columns:
        raise KeyError(
            f"Missing required transaction columns! Found columns: {list(df.columns)}. "
            "Ensure CSV contains 'sender' and 'receiver' (or 'sender_id' and 'receiver_id')."
        )

    G = nx.DiGraph()

    for _, row in df.iterrows():
        sender = str(row['sender'])
        receiver = str(row['receiver'])
        amount = row.get('amount', 0)

        G.add_edge(sender, receiver, amount=amount, type='transaction')

        if 'ip' in df.columns and pd.notna(row.get('ip')):
            ip = str(row['ip'])
            G.add_edge(sender, ip, type='uses_ip')
            G.add_edge(ip, sender, type='used_by')

        if 'device_id' in df.columns and pd.notna(row.get('device_id')):
            device = str(row['device_id'])
            G.add_edge(sender, device, type='uses_device')
            G.add_edge(device, sender, type='used_by')

    return G


def analyze_fraud_network(G):
    suspicious_nodes = []

    for node in G.nodes():
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)

        if in_deg >= 3 and out_deg <= 1:
            suspicious_nodes.append((node, "Mule Aggregation Hub (Smurfing Target)"))

    circular_loops = list(nx.simple_cycles(G))

    return suspicious_nodes, circular_loops


@tool("Analyze Fraud Network Tool")
def analyze_fraud_network_tool(csv_path: str) -> str:
    """Parses a transaction CSV file, constructs a directed entity graph, and detects structural fraud anomalies."""
    G = build_fraud_graph(csv_path)
    suspicious_nodes, circular_loops = analyze_fraud_network(G)
    return f"Suspicious Nodes: {suspicious_nodes}\nCircular Laundering Loops: {circular_loops}"


def generate_interactive_graph_html(G, suspicious_nodes=None):
    if suspicious_nodes is None:
        suspicious_nodes = []

    flagged_ids = [str(n[0]) if isinstance(n, tuple) else str(n) for n in suspicious_nodes]

    net = Network(height="520px", width="100%", bgcolor="#0F172A", font_color="#F8FAFC", directed=True)

    # Configure Barnes-Hut physics engine for drag, bounce, and force layout
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=120,
        spring_strength=0.05,
        damping=0.09
    )

    for node in G.nodes():
        node_str = str(node)
        title = f"Entity: {node_str}"

        if node_str in flagged_ids:
            color = "#EF4444"  # Red
            size = 25
            shape = "dot"
            title += " (FLAGGED SUSPICIOUS)"
        elif '.' in node_str or node_str.startswith('192.') or node_str.startswith('IP_'):
            color = "#F59E0B"  # Amber
            size = 18
            shape = "diamond"
            title += " (IP Address)"
        elif node_str.startswith('DEV_') or 'DEVICE' in node_str.upper():
            color = "#A855F7"  # Purple
            size = 18
            shape = "square"
            title += " (Hardware Device)"
        else:
            color = "#3B82F6"  # Blue
            size = 20
            shape = "dot"
            title += " (Bank Account)"

        net.add_node(node_str, label=node_str, color=color, size=size, shape=shape, title=title)

    for u, v, data in G.edges(data=True):
        u_str, v_str = str(u), str(v)
        edge_type = data.get('type', 'transaction')
        if edge_type == 'transaction':
            amount = data.get('amount', 'N/A')
            net.add_edge(u_str, v_str, title=f"Transaction: ${amount}", color="#94A3B8", width=2, arrows="to")
        else:
            net.add_edge(u_str, v_str, title=f"Shared Link: {edge_type}", color="#64748B", width=1, dashes=True)

    return net.generate_html()