# extract_key_insights.py — V2 STRICT INVESTOR-GRADE VERSION
# NO LLM EXTRACTION — DETERMINISTIC ONLY

import sys
from pathlib import Path
import argparse
import re

sys.path.append(str(Path(__file__).resolve().parents[1]))


# ============================================================
# STRICT DETERMINISTIC INSIGHT EXTRACTOR
# ============================================================

def extract_insights_deterministic(text: str, doc_name: str) -> list[str]:
    """
    Strict, extractive insight extraction.
    - No LLM
    - No hallucination possible
    - Works with Markdown, bullets, FR/EN
    """

    insights = []

    # Split document into meaningful blocks (paragraphs / bullet groups)
    blocks = [
        b.strip()
        for b in re.split(r"\n{2,}", text)
        if len(b.strip()) > 120
    ]

    KEYWORDS = {
        "Market": [
            "market", "marché", "demand", "demande", "competition", "concurr",
            "growth", "croissance"
        ],
        "Regulation": [
            "regulation", "réglement", "law", "loi", "autorité", "authority",
            "compliance", "licence", "approval", "approval"
        ],
        "Operations": [
            "operation", "process", "manufactur", "supply", "production",
            "distribution", "logistics"
        ],
        "Financial": [
            "revenue", "cost", "margin", "profit", "expense",
            "chiffre", "coût", "rentabilité"
        ],
        "Risk": [
            "risk", "risque", "challenge", "threat", "uncertainty",
            "contraint", "exposure"
        ],
    }

    for block in blocks:
        block_lower = block.lower()

        for insight_type, words in KEYWORDS.items():
            if any(w in block_lower for w in words):
                insights.append(
                    f"""### Insight
Type: {insight_type}
Source: {doc_name}
Excerpt: "{block[:500].replace('"', "'")}"
Implication: Indicates {insight_type.lower()} relevance based on source document.
"""
                )
                break

        if len(insights) >= 5:
            break

    return insights


# ============================================================
# MAIN EXTRACTION PIPELINE
# ============================================================

def extract_key_insights(project_name: str):
    BASE = Path(f"projects/{project_name}")
    DOCS = BASE / "standardized/docs"
    OUT = BASE / "insights/key_insights.md"
    OUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Extracting STRICT GROUNDED insights for: {project_name}")
    print(f"   Documents directory: {DOCS}")

    if not DOCS.exists():
        raise RuntimeError("No standardized documents found. Aborting.")

    doc_files = list(DOCS.glob("*.md"))

    if not doc_files:
        raise RuntimeError("No markdown documents found. Aborting.")

    all_insights = ["# Key Insights\n"]

    for doc in doc_files:
        print(f"   📄 Processing: {doc.name}")

        text = doc.read_text(encoding="utf-8").strip()
        print(f"   🧪 DEBUG: text length = {len(text)}")

        if len(text) < 300:
            raise RuntimeError(
                f"Document '{doc.name}' is too short for investment analysis."
            )

        insights = extract_insights_deterministic(text, doc.name)
        print(f"   🧪 DEBUG: extracted {len(insights)} insights")

        if not insights:
            raise RuntimeError(
                f"No investment-relevant content found in '{doc.name}'. "
                "Document is not suitable for investor-grade analysis."
            )

        all_insights.append(f"\n## From {doc.name}\n")
        all_insights.extend(insights)

        print(f"   ✅ Extractive insights generated from {doc.name}")

    final_output = "\n".join(all_insights)
    OUT.write_text(final_output, encoding="utf-8")

    print(f"✅ Grounded insights saved: {OUT}")
    return final_output


# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract STRICT investor-grade insights (v2)"
    )
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    extract_key_insights(args.project)


if __name__ == "__main__":
    main()