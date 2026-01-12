# create_sample_financials.py
import pandas as pd
from pathlib import Path
import json

def create_sample_financial_model(project_name="current_project"):
    """Create a sample Excel financial model."""
    
    BASE = Path(f"projects/{project_name}/raw_docs")
    BASE.mkdir(parents=True, exist_ok=True)
    
    # Create sample financial data
    financial_data = {
        "Summary": pd.DataFrame({
            "Metric": ["Revenue", "EBITDA", "Net Income", "Gross Margin", "Operating Expenses"],
            "Year 1": [1250000, 250000, 150000, 0.75, 850000],
            "Year 2": [1680000, 420000, 280000, 0.77, 950000],
            "Year 3": [2250000, 630000, 420000, 0.78, 1100000]
        }),
        
        "Revenue_Detail": pd.DataFrame({
            "Product": ["Product A", "Product B", "Product C", "Services"],
            "Year 1": [500000, 400000, 300000, 50000],
            "Year 2": [700000, 550000, 350000, 80000],
            "Year 3": [1000000, 750000, 400000, 100000]
        }),
        
        "Assumptions": pd.DataFrame({
            "Assumption": ["Market Growth", "Price Increase", "Customer Growth", "Churn Rate"],
            "Value": ["12%", "5%", "25%", "8%"],
            "Notes": ["Annual market expansion", "Annual price adjustment", "New customers per year", "Annual churn"]
        })
    }
    
    # Save to Excel
    excel_path = BASE / "financial_model.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for sheet_name, df in financial_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"✅ Created sample financial model: {excel_path}")
    
    # Also create the JSON summary that extract_financials.py expects
    financial_dir = Path(f"projects/{project_name}/financial")
    financial_dir.mkdir(parents=True, exist_ok=True)
    
    summary_data = {
        "revenue": {
            "year_1": 1250000,
            "year_2": 1680000,
            "year_3": 2250000
        },
        "ebitda": {
            "year_1": 250000,
            "year_2": 420000,
            "year_3": 630000
        },
        "net_income": {
            "year_1": 150000,
            "year_2": 280000,
            "year_3": 420000
        }
    }
    
    summary_path = financial_dir / "summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"✅ Created financial summary: {summary_path}")
    
    return excel_path

if __name__ == "__main__":
    create_sample_financial_model()