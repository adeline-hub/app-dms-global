# setup_project.py
from pathlib import Path
import json

def setup_project_structure(project_name="current_project"):
    """Create the necessary directory structure for a project."""
    
    BASE = Path(f"projects/{project_name}")
    
    # Create all required directories
    directories = [
        BASE / "raw_docs",
        BASE / "standardized/docs",
        BASE / "insights",
        BASE / "memo",
        BASE / "financial",
        BASE / "financial/charts",
        BASE / "deck",
        BASE / "outputs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Create sample files if they don't exist
    sample_files = {
        BASE / "insights/key_insights.md": """# Key Insights

## Market Analysis
- The target market shows 12% annual growth (Source: market_report.pdf)
- Competitive landscape has 3 major players (Source: competitive_analysis.docx)

## Financial Projections
- Revenue projected to grow at 15% CAGR (Source: financial_model.xlsx)
- EBITDA margins expected around 22% (Source: financial_model.xlsx)

## Business Model
- SaaS subscription model with 90% retention (Source: business_plan.pdf)
- Clear path to profitability in 18 months (Source: business_plan.pdf)""",
        
        BASE / "financial/summary.json": """{
  "revenue": {
    "year_1": 1250000,
    "year_2": 1680000,
    "year_3": 2250000
  },
  "ebitda": {
    "year_1": 250000,
    "year_2": 420000,
    "year_3": 630000
  }
}""",
        
        BASE / "memo/structure_overview.md": """# Structure Overview

## Legal Structure
- Delaware C-Corporation
- Clean cap table with founder control

## Governance
- Board of 5 directors (2 independent)
- Quarterly board meetings
- Audit committee established

## Economics
- SaaS model with tiered pricing
- 80% gross margins
- Recurring revenue model""",
        
        BASE / "memo/market_analysis.md": """# Market Analysis

## Market Size
- TAM: $2.5B
- SAM: $850M
- SOM: $125M (Year 1 target)

## Growth Rate
- 12% annual market growth
- Digital transformation driving demand

## Competitive Landscape
- 3 major incumbents
- Fragmented mid-market""",
        
        BASE / "deck/deck.md": """# Business Deck

## Executive Summary
Innovative SaaS platform disrupting the market with strong growth potential.

## Market Opportunity
$2.5B market growing at 12% annually.

## Financial Projections
- Year 1: $1.25M revenue
- Year 2: $1.68M revenue  
- Year 3: $2.25M revenue

## Investment Ask
$2M seed round for product development and market expansion."""
    }
    
    for file_path, content in sample_files.items():
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")
            print(f"📄 Created sample: {file_path}")
    
    print(f"\n✅ Project structure created for '{project_name}'")

if __name__ == "__main__":
    setup_project_structure()