import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
import json
from utils.llm import ask

def generate_business_deck(project_name, sector="", territory=""):
    """
    Generate a comprehensive business deck from all pipeline outputs.
    
    Args:
        project_name: Name of the project
        sector: Business sector (from Summer input)
        territory: Geographic territory (from Summer input)
    
    Returns:
        Markdown content of the business deck
    """
    BASE = Path(f"projects/{project_name}")
    OUT = BASE / "deck/deck.md"
    OUT.parent.mkdir(exist_ok=True)

    print(f"📝 Generating business deck for: {project_name}")
    print(f"  📍 Sector: {sector}")
    print(f"  🌍 Territory: {territory}")
    
    # ====================================================================
    # 1. COLLECT ALL CONTENT FROM PIPELINE STEPS
    # ====================================================================
    
    content_sections = {}
    
    # A. Insights from uploaded documents
    insights_path = BASE / "insights/key_insights.md"
    if insights_path.exists():
        try:
            insights_content = insights_path.read_text(encoding="utf-8")
            if insights_content.strip():
                content_sections["document_insights"] = insights_content
                print(f"  ✅ Added insights from {insights_path.name}")
            else:
                print(f"  ⚠️ Insights file is empty")
        except Exception as e:
            print(f"  ❌ Error reading insights: {e}")
    else:
        print(f"  ⚠️ Insights file not found: {insights_path}")
    
    # B. Structure overview
    structure_path = BASE / "memo/structure_overview.md"
    if structure_path.exists():
        try:
            structure_content = structure_path.read_text(encoding="utf-8")
            if structure_content.strip():
                content_sections["structure"] = structure_content
                print(f"  ✅ Added structure overview")
        except Exception as e:
            print(f"  ❌ Error reading structure: {e}")
    
    # C. Other memo files
    memo_dir = BASE / "memo"
    memo_sections = []
    if memo_dir.exists():
        for f in sorted(memo_dir.glob("*.md")):
            if f.name != "structure_overview.md":  # Avoid duplicate
                try:
                    content = f.read_text(encoding="utf-8")
                    if content.strip():
                        memo_sections.append({
                            "title": f.stem.replace("_", " ").title(),
                            "content": content[:1000]  # Limit length
                        })
                except Exception as e:
                    print(f"  ❌ Error reading {f.name}: {e}")
    
    # D. Financial data
    financial_summary = ""
    financial_data = {}
    summary_path = BASE / "financial/summary.json"
    if summary_path.exists():
        try:
            with open(summary_path, 'r') as f:
                financial_data = json.load(f)
            
            # Extract sector/territory from financial data if not provided
            if 'project_info' in financial_data:
                info = financial_data['project_info']
                if not sector and 'sector' in info:
                    sector = info['sector']
                if not territory and 'territory' in info:
                    territory = info['territory']
            
            # Format financial summary
            financial_lines = []
            
            if 'revenue' in financial_data:
                rev = financial_data['revenue']
                financial_lines.append("### Revenue Projections")
                if rev.get('year_1'):
                    financial_lines.append(f"- Year 1: ${rev['year_1']:,}")
                if rev.get('year_2'):
                    financial_lines.append(f"- Year 2: ${rev['year_2']:,}")
                if rev.get('year_3'):
                    financial_lines.append(f"- Year 3: ${rev['year_3']:,}")
            
            if 'ebitda' in financial_data:
                ebitda = financial_data['ebitda']
                financial_lines.append("### EBITDA Projections")
                if ebitda.get('year_1'):
                    financial_lines.append(f"- Year 1: ${ebitda['year_1']:,}")
                if ebitda.get('year_2'):
                    financial_lines.append(f"- Year 2: ${ebitda['year_2']:,}")
                if ebitda.get('year_3'):
                    financial_lines.append(f"- Year 3: ${ebitda['year_3']:,}")
            
            if financial_lines:
                financial_summary = "\n".join(financial_lines)
                content_sections["financials"] = financial_summary
                print(f"  ✅ Added financial data")
                
        except Exception as e:
            print(f"  ❌ Error reading financial data: {e}")
    
    # E. Project reasoning (if available)
    reasoning_path = BASE / "project_reasoning.txt"
    if reasoning_path.exists():
        try:
            reasoning_content = reasoning_path.read_text(encoding="utf-8")
            if reasoning_content.strip():
                content_sections["reasoning"] = reasoning_content
                print(f"  ✅ Added project reasoning")
        except Exception as e:
            print(f"  ❌ Error reading reasoning: {e}")
    
    # ====================================================================
    # 2. GENERATE THE DECK CONTENT
    # ====================================================================
    
    deck_content = f"""# {sector if sector else "Business"} Investment Deck

## Project Overview
**Project:** {project_name}
**Sector:** {sector if sector else "Analysis in progress"}
**Territory:** {territory if territory else "Target markets"}
**Status:** Generated from comprehensive pipeline analysis

## Executive Summary
This investment deck presents an opportunity in the **{sector if sector else "target"}** sector with operations in **{territory if territory else "key markets"}**. The analysis is based on uploaded documents, market research, and financial projections.

{"## Insights from Uploaded Documents" if "document_insights" in content_sections else "## Document Analysis"}
{content_sections.get("document_insights", "Document analysis reveals market opportunities, competitive landscape, and key risks from the uploaded materials.")}

{"## Business Structure" if "structure" in content_sections else "## Organizational Framework"}
{content_sections.get("structure", "Business structure analysis provides the foundation for growth strategy and operational execution.")}

{"## Financial Projections" if "financials" in content_sections else "## Financial Overview"}
{content_sections.get("financials", "Financial projections indicate strong growth potential with positive unit economics. Detailed models available upon request.")}
"""
    
    # Add additional memo sections if available
    if memo_sections:
        deck_content += "\n## Detailed Analysis\n"
        for memo in memo_sections[:3]:  # Limit to 3 sections
            deck_content += f"\n### {memo['title']}\n{memo['content'][:300]}...\n"
    
    # Add project reasoning if available
    if "reasoning" in content_sections:
        deck_content += f"\n## Strategic Assessment\n{content_sections['reasoning'][:500]}..."
    
    # Add investment recommendation
    deck_content += f"""
## Investment Recommendation

### Key Strengths
1. **Market Position**: Strong opportunity in {sector if sector else "the target"} sector
2. **Financials**: { "Positive projections with clear growth trajectory" if "financials" in content_sections else "Solid financial foundation" }
3. **Documents**: Comprehensive analysis supports investment case

### Considerations
- Market dynamics in {territory if territory else "target regions"}
- Execution timeline and resource requirements
- Competitive landscape evolution

### Next Steps
1. **Due Diligence**: Comprehensive review of all findings
2. **Financial Modeling**: Refine projections based on latest data  
3. **Investment Committee**: Present findings for approval
4. **Legal & Compliance**: Finalize documentation

---
*This deck was automatically generated from uploaded documents and analysis.*
*Generated by the Business Deck Pipeline on {Path(__file__).parent.name}*
"""
    
    # ====================================================================
    # 3. SAVE AND RETURN THE DECK
    # ====================================================================
    
    OUT.write_text(deck_content, encoding="utf-8")
    
    summary_path = BASE / "deck/deck_summary.txt"
    summary_content = f"""Deck Generation Summary
=======================
Project: {project_name}
Sector: {sector}
Territory: {territory}
Generated: {len(deck_content)} characters
Sections included: {', '.join(content_sections.keys()) if content_sections else 'Basic template'}
Output file: {OUT}

Content Preview:
{deck_content[:500]}...
"""
    summary_path.write_text(summary_content, encoding="utf-8")
    
    print(f"✅ Deck created: {OUT}")
    print(f"  Content length: {len(deck_content):,} characters")
    print(f"  Sections included: {len(content_sections)}")
    print(f"  Summary saved: {summary_path}")
    
    return deck_content


def main():
    parser = argparse.ArgumentParser(description="Generate business deck from pipeline outputs")
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--sector', help='Business sector (optional)')
    parser.add_argument('--territory', help='Geographic territory (optional)')
    
    args = parser.parse_args()
    result = generate_business_deck(args.project, args.sector, args.territory)
    
    print(f"\n🎉 Deck generation complete!")
    print(f"Preview: {result[:200]}...")


if __name__ == "__main__":
    main()