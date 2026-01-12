import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from utils.llm import ask

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    args = parser.parse_args()

    BASE = Path(f"projects/{args.project}")
    INSIGHTS = (BASE / "insights/key_insights.md").read_text(encoding="utf-8")
    MEMO = BASE / "memo"
    MEMO.mkdir(exist_ok=True)

    sections = {
        "01_overview.md": "Write an executive overview.",
        "02_market.md": "Expand the market analysis.",
        "03_regulation.md": "Explain regulatory considerations.",
        "04_business_model.md": "Describe the business model.",
        "05_risks.md": "Detail key risks.",
    }

    for file, instruction in sections.items():
        prompt = f"""
    Using the insights below, {instruction}

    Insights:
    {INSIGHTS}
    """
        text = ask(prompt)
        (MEMO / file).write_text(text, encoding="utf-8")

    print("LLM memo generated")

if __name__ == "__main__":
    main()