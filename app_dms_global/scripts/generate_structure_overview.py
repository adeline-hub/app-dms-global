import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from utils.llm import ask

def generate_structure_overview(project_name):  # <-- Accept project_name as parameter
    BASE = Path(f"projects/{project_name}")
    INSIGHTS = (BASE / "insights/key_insights.md").read_text(encoding="utf-8")
    OUT = BASE / "memo/structure_overview.md"

    prompt = f"""
    Based on the following insights, describe:
    - Legal structure
    - Governance
    - Economics
    - Market opportunities
    - Competitive landscape
    - Financial projections
    - kpi's
    - Funding requirements
    - Key constraints

    Insights:
    {INSIGHTS}
    """

    OUT.write_text(ask(prompt), encoding="utf-8")
    print("LLM structure overview generated")

def main():  # <-- Separate main function for CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    args = parser.parse_args()
    
    # Call the actual function with the argument
    generate_structure_overview(args.project)

if __name__ == "__main__":
    main()  # <-- Only runs when script is executed directly