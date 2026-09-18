========================================================================
PROJECT F.I.N.D. — Financial Investigation & Network Discovery
Autonomous Multi-Agent Fraud Network Detection & Compliance System
========================================================================

OVERVIEW
------------------------------------------------------------------------
Project F.I.N.D. replaces isolated transaction-level rules with graph 
network analysis and multi-agent AI reasoning. It identifies hidden multi-entity
relationships (shared IPs, shared devices, and circular funding loops) across
accounts and generates regulatory-grade Suspicious Activity Reports (SARs).

SYSTEM ARCHITECTURE & FILE STRUCTURE
------------------------------------------------------------------------
├── .env                  # Environment keys (GROQ_API_KEY / GEMINI_API_KEY)
├── requirements.txt      # Project dependencies
├── tools.py              # NetworkX graph analysis tools & entity discovery logic
├── agent.py              # CrewAI multi-agent orchestration (Investigator & Compliance)
├── app.py                # Streamlit command center and graph visualizer
├── generate_pdf.py       # ReportLab PDF report generation engine
└── transactions.csv      # Sample financial transaction dataset

PREREQUISITES & ENVIRONMENT SETUP
------------------------------------------------------------------------
* Python Version: Python 3.10 or Python 3.11 is recommended.
* Recommended API: Groq API Key (Free, fast inference via Llama-3) or Gemini API Key.

1. Create and activate a Python virtual environment:
   Windows:
     py -3.11 -m venv .venv
     .venv\Scripts\activate
   
   macOS/Linux:
     python3.11 -m venv .venv
     source .venv/bin/activate

2. Install required dependencies:
   pip install -r requirements.txt

3. Create a .env file in the project root:
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here

RUNNING THE APPLICATION
------------------------------------------------------------------------
Launch the interactive Streamlit command center:

   streamlit run app.py

Once launched, navigate to http://localhost:8501 in your browser to:
1. View the raw ledger and live entity network topology graph.
2. Trigger the autonomous multi-agent investigation pipeline.
3. Download synthesized SAR Markdown reports and evaluation PDFs.

EVALUATION & PDF REPORT GENERATION
------------------------------------------------------------------------
To independently generate the benchmark evaluation PDF:

   python generate_pdf.py

This generates 'FIND_Evaluation_Report.pdf' detailing precision scores, 
typology classification rates, and execution time metrics.