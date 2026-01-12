# create_sample_deck.py
from pathlib import Path

def create_sample_deck(project_name="current_project"):
    BASE = Path(f"projects/{project_name}")
    DECK = BASE / "deck/deck.md"
    DECK.parent.mkdir(parents=True, exist_ok=True)
    
    sample_content = """# TechSaaS Investment Deck

## Executive Summary
Innovative SaaS platform for the digital transformation market.
Strong product-market fit with 15% monthly growth.

## Market Opportunity
- Total Addressable Market: $2.5B
- Serviceable Addressable Market: $850M
- Annual Growth: 12%
- Fragmented competitive landscape

## Product Solution
- Cloud-native SaaS platform
- AI-powered analytics
- Enterprise-grade security
- Scalable architecture

## Business Model
- Subscription-based pricing
- Tiered plans (Basic, Pro, Enterprise)
- 90% customer retention rate
- 80% gross margins

## Financial Projections
### Revenue
- Year 1: $1.25M
- Year 2: $1.68M
- Year 3: $2.25M

### Profitability
- EBITDA positive in Year 2
- 25% EBITDA margin by Year 3
- Strong cash flow generation

## Team
- CEO: Former tech executive (10+ years)
- CTO: Ex-Google engineer
- CRO: Sales leader with enterprise experience

## Investment Ask
- Seed Round: $2M
- Use of Funds: Product development (40%), Sales (30%), Marketing (20%), Operations (10%)
- Valuation: $10M pre-money"""
    
    DECK.write_text(sample_content, encoding="utf-8")
    print(f"✅ Created sample deck: {DECK}")

if __name__ == "__main__":
    create_sample_deck()