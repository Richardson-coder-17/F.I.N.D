import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import analyze_fraud_network_tool

def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    return LLM(
        model="gemini/gemini-3.1-flash-lite",
        api_key=api_key
    )

def run_fraud_investigation(csv_path: str):
    llm = get_llm()

    network_analyst = Agent(
        role="Senior Financial Network Analyst",
        goal="Extract topological anomalies, circular loops, and smurfing funnels from transaction data.",
        backstory="Expert in forensic graph analysis, mapping multi-hop money laundering networks and shared device/IP infrastructure.",
        tools=[analyze_fraud_network_tool],
        llm=llm,
        verbose=True
    )

    compliance_officer = Agent(
        role="Chief AML Compliance Officer",
        goal="Synthesize network findings into an official regulatory Suspicious Activity Report (SAR).",
        backstory="Former regulatory investigator specialized in FinCEN SAR drafting, risk assessment, and action recommendations.",
        llm=llm,
        verbose=True
    )

    task_analyze = Task(
        description=f"Analyze the financial transaction network in '{csv_path}' using the Analyze Fraud Network Tool. Identify high-risk nodes, smurfing targets, and circular money flows.",
        expected_output="Detailed breakdown of network topology, flagged accounts, and identified laundering patterns.",
        agent=network_analyst
    )

    task_report = Task(
        description="Review the analyst's network findings and generate a formal Suspicious Activity Report (SAR) in Markdown format. Include Executive Summary, Flagged Entities, Detected Patterns, and Recommended Actions.",
        expected_output="Comprehensive Suspicious Activity Report (SAR) formatted in Markdown.",
        agent=compliance_officer
    )

    crew = Crew(
        agents=[network_analyst, compliance_officer],
        tasks=[task_analyze, task_report],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff()
