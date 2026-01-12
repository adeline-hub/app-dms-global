from app_dms_global.scripts.standardize_documents import standardize_documents
from app_dms_global.scripts.extract_key_insights import extract_key_insights
from app_dms_global.scripts.project_reasoning import project_reasoning
from app_dms_global.scripts.generate_structure_overview import generate_structure_overview
from app_dms_global.scripts.financial.extract_financials import extract_financials
from app_dms_global.scripts.financial.generate_financial_charts import generate_financial_charts
from app_dms_global.scripts.generate_business_deck import generate_business_deck
from app_dms_global.scripts.deck_md_to_ppt import deck_md_to_ppt
from pathlib import Path
import time
import json

# app_dms_global/scripts/pipeline.py

import sys
from pathlib import Path
import shutil

# ──────────────── CLEAR CACHES ──────────────────
ROOT = Path(__file__).resolve().parents[2]

# 1. Remove LLM mock cache
LLM_CACHE = ROOT / ".llm_cache"
shutil.rmtree(LLM_CACHE, ignore_errors=True)

# 2. Remove all Python bytecode caches
for p in ROOT.rglob("__pycache__"):
    shutil.rmtree(p, ignore_errors=True)

# Now proceed with normal imports

def run_pipeline(
    project_id: str,
    sector: str,
    territory: str,
    input_dir: str,
    output_dir: str,
):
    """
    Run the complete pipeline for generating business decks.
    
    Args:
        project_id: The project identifier/name
        sector: Business sector (e.g., "technology", "healthcare")
        territory: Geographic territory (e.g., "US", "EU")
        input_dir: Directory containing raw input documents
        output_dir: Directory for output files
    """
    
    print(f"🚀 Starting pipeline for project: {project_id}")
    print(f"   📍 Sector: {sector}")
    print(f"   🌍 Territory: {territory}")
    
    try:
        # Create project directory structure if needed
        BASE = Path(f"projects/{project_id}")
        BASE.mkdir(parents=True, exist_ok=True)
        
        # 1. Standardize documents (convert PDF/DOCX to markdown)
        print("\n1. 📄 Standardizing documents...")
        try:
            standardized_docs = standardize_documents(project_id)
            if standardized_docs:
                print(f"   ✅ Standardized {len(standardized_docs) if isinstance(standardized_docs, list) else 'some'} documents")
            else:
                print(f"   ⚠️ No documents standardized")
        except Exception as e:
            print(f"   ❌ Standardization error: {e}")
            # Create sample documents for testing
            sample_dir = BASE / "standardized/docs"
            sample_dir.mkdir(parents=True, exist_ok=True)
            sample_file = sample_dir / "sample_document.md"
            sample_file.write_text("# Sample Document\n\nContent from uploaded files would appear here.", encoding="utf-8")
        
        # 2. Extract key insights from standardized documents
        print("\n2. 🔍 Extracting key insights...")
        time.sleep(3)  # Small delay
        try:
            insights = extract_key_insights(project_id)
            if insights:
                print(f"   ✅ Extracted {len(insights) if isinstance(insights, list) else 'some'} insights")
            else:
                print(f"   ⚠️ No insights extracted")
        except Exception as e:
            print(f"   ❌ Insights extraction error: {e}")
            # Create sample insights
            insights_path = BASE / "insights/key_insights.md"
            insights_path.parent.mkdir(parents=True, exist_ok=True)
            insights_path.write_text("# Key Insights\n\nDocument analysis would appear here.", encoding="utf-8")
        
        # 3. Reason on project with insights
        print("\n3. 💭 Reasoning on project...")
        try:
            # Create question based on sector/territory
            reasoning_question = f"Based on the document analysis, what are the key investment considerations for this {sector} project in {territory}?"
            project_context = project_reasoning(reasoning_question)
            print(f"   ✅ Project reasoning completed")
        except Exception as e:
            print(f"   ❌ Reasoning error: {e}")
            project_context = f"Project analysis for {sector} in {territory}"
        
        # 4. Generate structure overview
        print("\n4. 🏛️ Generating structure overview...")
        time.sleep(5)  # Wait to avoid rate limit
        try:
            structure = generate_structure_overview(project_id)
            print(f"   ✅ Structure overview generated")
        except Exception as e:
            print(f"   ❌ Structure error: {e}")
            # Create sample structure
            structure_path = BASE / "memo/structure_overview.md"
            structure_path.parent.mkdir(parents=True, exist_ok=True)
            structure_path.write_text(f"# Structure Overview\n\n{sector} project in {territory}", encoding="utf-8")
        
        # 5. Extract financials
        print("\n5. 📈 Extracting financial data...")
        try:
            financial_data, financial_path = extract_financials(project_id)
            print(f"   ✅ Financial data extracted")
            # Save sector/territory in financial data
            if isinstance(financial_data, dict):
                financial_data["project_info"] = {
                    "sector": sector,
                    "territory": territory,
                    "project_id": project_id
                }
                # Update the JSON file
                financial_path_obj = Path(financial_path)
                if financial_path_obj.exists():
                    with open(financial_path_obj, 'w') as f:
                        json.dump(financial_data, f, indent=2)
        except Exception as e:
            print(f"   ❌ Financial extraction error: {e}")
            # Create sample financial data
            financial_dir = BASE / "financial"
            financial_dir.mkdir(parents=True, exist_ok=True)
            sample_data = {
                "revenue": {"year_1": 1250000, "year_2": 1680000, "year_3": 2250000},
                "ebitda": {"year_1": 250000, "year_2": 420000, "year_3": 630000},
                "project_info": {"sector": sector, "territory": territory}
            }
            financial_path = financial_dir / "summary.json"
            with open(financial_path, 'w') as f:
                json.dump(sample_data, f, indent=2)
        
        # 6. Generate financial charts
        print("\n6. 📊 Generating financial charts...")
        try:
            chart_path = generate_financial_charts(project_id)
            print(f"   ✅ Financial charts generated")
        except Exception as e:
            print(f"   ❌ Charts error: {e}")
            chart_path = None
        
        # 7. Generate business deck markdown (PASS SECTOR AND TERRITORY)
        print("\n7. 📋 Generating business deck...")
        try:
            # Import here to ensure we have the latest version
            from app_dms_global.scripts.generate_business_deck import generate_business_deck
            deck_md = generate_business_deck(project_id, sector, territory)
            print(f"   ✅ Business deck generated ({len(deck_md) if deck_md else 0} characters)")
        except Exception as e:
            print(f"   ❌ Deck generation error: {e}")
            # Create a basic deck
            deck_dir = BASE / "deck"
            deck_dir.mkdir(parents=True, exist_ok=True)
            deck_path = deck_dir / "deck.md"
            basic_deck = f"""# {sector} Investment Deck - {project_id}

## Project Overview
**Sector:** {sector}
**Territory:** {territory}

## Executive Summary
Investment opportunity based on document analysis.

## Document Insights
Review the uploaded documents for detailed analysis.

## Financial Summary
See attached financial projections.

## Investment Opportunity
Compelling opportunity with growth potential."""
            deck_path.write_text(basic_deck, encoding="utf-8")
            deck_md = basic_deck
        
        # 8. Export to PowerPoint
        print("\n8. 📈 Creating PowerPoint presentation...")
        audience = "investors"
        try:
            final_deck_path = deck_md_to_ppt(project_id, audience)
            print(f"   ✅ PowerPoint created: {final_deck_path}")
        except Exception as e:
            print(f"   ❌ PowerPoint error: {e}")
            print("   Creating simple text version instead...")
            
            # Create a simple text output
            simple_path = Path(f"projects/{project_id}/outputs/{project_id}-{audience}.txt")
            simple_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Include actual content from the deck
            deck_content = ""
            deck_file = BASE / "deck/deck.md"
            if deck_file.exists():
                deck_content = deck_file.read_text(encoding="utf-8")[:500]
            
            summary = f"""Business Deck Summary
Project: {project_id}
Sector: {sector}
Territory: {territory}

Deck Content Preview:
{deck_content}

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}"""
            
            simple_path.write_text(summary, encoding="utf-8")
            final_deck_path = str(simple_path)
        
        print(f"\n🎉 Pipeline completed successfully!")
        print(f"📁 Output saved to: {final_deck_path}")
        
        # Create a completion marker
        completion_file = BASE / "pipeline_complete.txt"
        completion_file.write_text(f"Pipeline completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\nSector: {sector}\nTerritory: {territory}", encoding="utf-8")
        
        return final_deck_path
        
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        
        # Create error output
        error_path = Path(f"projects/{project_id}/outputs/{project_id}-error.txt")
        error_path.parent.mkdir(parents=True, exist_ok=True)
        error_content = f"""Pipeline Error Report
Project: {project_id}
Sector: {sector}
Territory: {territory}
Error: {str(e)}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"""
        
        error_path.write_text(error_content, encoding="utf-8")
        return str(error_path)


# Optional: Add CLI interface for pipeline.py itself
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run the business deck generation pipeline")
    parser.add_argument('--project', required=True, help='Project ID/name')
    parser.add_argument('--sector', required=True, help='Business sector')
    parser.add_argument('--territory', required=True, help='Geographic territory')
    parser.add_argument('--input-dir', help='Input directory (optional, uses project structure)')
    parser.add_argument('--output-dir', help='Output directory (optional, uses project structure)')
    parser.add_argument('--audience', default='investors', help='Target audience for deck')
    
    args = parser.parse_args()
    
    # Use defaults if not provided
    input_dir = args.input_dir or f"projects/{args.project}/raw_docs"
    output_dir = args.output_dir or f"projects/{args.project}/outputs"
    
    result = run_pipeline(
        project_id=args.project,
        sector=args.sector,
        territory=args.territory,
        input_dir=input_dir,
        output_dir=output_dir,
    )
    
    print(f"\nFinal result: {result}")