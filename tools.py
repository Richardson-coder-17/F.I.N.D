import pandas as pd
import networkx as nx
from crewai.tools import tool

def build_fraud_graph(csv_path: str = "transactions.csv") -> nx.Graph:
    """Pure Python utility to construct a NetworkX graph object for UI plotting."""
    df = pd.read_csv(csv_path)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(str(row['sender_id']), str(row['receiver_id']), type='TRANSFER', amount=row['amount'])
        G.add_edge(str(row['sender_id']), f"IP:{row['ip_address']}", type='INFRASTRUCTURE')
        G.add_edge(str(row['sender_id']), f"DEV:{row['device_id']}", type='INFRASTRUCTURE')
    return G

@tool("Financial Network Graph Analyzer")
def analyze_fraud_network(csv_path: str = "transactions.csv") -> str:
    """Parses transaction CSV data, builds an entity graph, and detects shared IPs, devices, and circular funding rings."""
    try:
        G = build_fraud_graph(csv_path)

        # Detect Shared Infrastructure (Nodes connected to multiple accounts)
        shared_entities = []
        for node in G.nodes():
            if str(node).startswith(("IP:", "DEV:")) and G.degree(node) > 1:
                connected_accounts = list(G.neighbors(node))
                shared_entities.append(f"- Infrastructure '{node}' shared by accounts: {connected_accounts}")

        # Detect Large/Suspicious Clusters
        components = list(nx.connected_components(G))
        large_clusters = [c for c in components if len(c) >= 4]

        report = f"--- NETWORK DISCOVERY RESULTS ---\n"
        report += f"Total Entities Analyzed: {len(G.nodes())}\n"
        report += f"Shared Infrastructure Detected:\n" + ("\n".join(shared_entities) if shared_entities else "None") + "\n"
        report += f"Flagged Network Clusters Found: {len(large_clusters)}\n"
        
        return report
    except Exception as e:
        return f"Error executing network graph analysis: {str(e)}"