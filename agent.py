import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import analyze_fraud_network

gemini_llm = LLM(
        model="gemini/gemini-3.1-flash-lite",
        api_key=os.getenv("Gemini_api_key")
)

def run_fraud_investigation(csv_path: str = "transactions.csv"):
    # Agent 1: Network Investigator
    graph_agent = Agent(
        role="Network Graph Investigator",
        goal="Identify hidden connections, shared devices, and multi-hop funding loops in financial logs.",
        backstory="An expert forensic analyst specializing in graph analysis and fraud ring discovery.",
        tools=[analyze_fraud_network],
        llm=gemini_llm,
        verbose=True
    )

    # Agent 2: Compliance Specialist
    compliance_agent = Agent(
        role="Financial Crime & SAR Specialist",
        goal="Synthesize network findings into an official Suspicious Activity Report (SAR).",
        backstory="A senior compliance officer who drafts regulatory reports with evidence trails.",
        llm=gemini_llm,
        verbose=True
    )

    # Tasks
    task_investigate = Task(
        description=f"Analyze the dataset at '{csv_path}' using the Network Graph Tool. Identify all shared infrastructure and flagged clusters.",
        expected_output="Detailed list of connected accounts, shared IPs, and suspicious cluster nodes.",
        agent=graph_agent
    )

    task_sar_report = Task(
        description="Convert the network investigation findings into a formal Suspicious Activity Report (SAR) detailing: 1. Executive Summary, 2. Identified Fraud Ring, 3. Evidence Matrix, and 4. Recommended Action (Freeze/Flag).",
        expected_output="A structured markdown SAR report.",
        agent=compliance_agent
    )

    crew = Crew(
        agents=[graph_agent, compliance_agent],
        tasks=[task_investigate, task_sar_report],
        process=Process.sequential
    )

    return crew.kickoff()