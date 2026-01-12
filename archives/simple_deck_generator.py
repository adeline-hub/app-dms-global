# simple_deck_generator.py
from pathlib import Path
import json

def create_guaranteed_deck(project_name, sector, territory):
    """Create a deck that always has content."""
    
    BASE = Path(f"projects/{project_name}")
    DECK = BASE / "deck/deck.md"
    DECK.parent.mkdir(parents=True, exist_ok=True)
    
    # Read financial data if exists
    financial_info = ""
    financial_path = BASE / "financial/summary.json"
    if financial_path.exists():
        try:
            with open(financial_path, 'r') as f:
                data = json.load(f)
                if 'revenue' in data:
                    rev = data['revenue']
                    financial_info = f"""
### Financial Projections
- Year 1 Revenue: ${rev.get('year_1', 0):,}
- Year 2 Revenue: ${rev.get('year_2', 0):,}
- Year 3 Revenue: ${rev.get('year_3', 0):,}
"""
        except:
            pass
    
    # Create deck content
    deck_content = f"""# {sector.title() if sector else "Business"} Investment Opportunity

## Project: {project_name}
**Sector:** {sector if sector else "Not specified"}
**Territory:** {territory if territory else "Not specified"}

## Executive Summary
This investment deck presents an opportunity in the {sector if sector else "target"} sector operating in {territory if territory else "key markets"}.

## Market Analysis
The {sector if sector else "target"} market in {territory if territory else "the region"} shows strong growth potential with increasing demand for innovative solutions.

## Business Model
Scalable business model with multiple revenue streams and strong unit economics.

{financial_info}

## Investment Ask
Seed funding required to accelerate growth and capture market opportunity.

## Team
Experienced leadership team with relevant industry background.

## Next Steps
- Due diligence completion
- Financial modeling
- Investment committee review"""
    
    DECK.write_text(deck_content, encoding="utf-8")
    print(f"✅ Created guaranteed deck: {DECK}")
    return str(DECK)

if __name__ == "__main__":
    # Test with sample data
    create_guaranteed_deck("current_project", "Technology", "Europe")