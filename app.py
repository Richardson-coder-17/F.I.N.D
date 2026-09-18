import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from dotenv import load_dotenv

from tools import build_fraud_graph
from agent import run_fraud_investigation

load_dotenv()

st.set_page_config(page_title="F.I.N.D. — Fraud Network Discovery", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ Project F.I.N.D.")
st.caption("Financial Investigation & Network Discovery via Autonomous Agentic Graph Intelligence")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")
csv_file = st.sidebar.file_uploader("Upload Transaction CSV", type=["csv"])

# Default fallback dataset generator
DEFAULT_CSV = "transactions.csv"
if not os.path.exists(DEFAULT_CSV):
    sample_df = pd.DataFrame([
        {"tx_id": "TX101", "sender_id": "ACC_101", "receiver_id": "ACC_102", "amount": 5000, "ip_address": "192.168.1.1", "device_id": "DEV_88"},
        {"tx_id": "TX102", "sender_id": "ACC_102", "receiver_id": "ACC_103", "amount": 4900, "ip_address": "192.168.1.1", "device_id": "DEV_88"},
        {"tx_id": "TX103", "sender_id": "ACC_103", "receiver_id": "ACC_101", "amount": 4800, "ip_address": "192.168.1.1", "device_id": "DEV_99"},
        {"tx_id": "TX104", "sender_id": "ACC_201", "receiver_id": "ACC_202", "amount": 150, "ip_address": "10.0.0.5", "device_id": "DEV_12"}
    ])
    sample_df.to_csv(DEFAULT_CSV, index=False)

target_csv = DEFAULT_CSV
if csv_file is not None:
    target_csv = "uploaded_transactions.csv"
    with open(target_csv, "wb") as f:
        f.write(csv_file.getbuffer())

# Layout Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Raw Transaction Ledger")
    df = pd.read_csv(target_csv)
    st.dataframe(df, use_container_width=True)

    st.subheader("🌐 Entity Network Topology")
    G = build_fraud_graph(target_csv)
    
    # Render Matplotlib Network Graph
    fig, ax = plt.subplots(figsize=(8, 5))
    pos = nx.spring_layout(G, seed=42)
    
    # Node Coloring: Red for IPs/Devices, Blue for Accounts
    color_map = ['#ff4b4b' if str(node).startswith(("IP:", "DEV:")) else '#1c83e1' for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='#cccccc', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='white', font_weight='bold', ax=ax)
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    plt.axis('off')
    st.pyplot(fig)

with col2:
    st.subheader("🤖 Autonomous Investigation")
    
    if st.button("Run Multi-Agent Investigation", type="primary", use_container_width=True):
        if not os.getenv("GEMINI_API_KEY"):
            st.error("Missing GEMINI_API_KEY! Please set it in your .env file.")
        else:
            with st.spinner("Agents Analyzing Graph Topology & Formulating SAR..."):
                try:
                    result = run_fraud_investigation(target_csv)
                    sar_report = str(result)
                    
                    st.success("Investigation Complete!")
                    st.markdown("---")
                    st.markdown(sar_report)
                    
                    # Download SAR Button
                    st.download_button(
                        label="📥 Download SAR Report (.md)",
                        data=sar_report,
                        file_name="Suspicious_Activity_Report_FIND.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Investigation Failed: {str(e)}")