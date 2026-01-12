# debug_deck.py
from pathlib import Path
import json

def debug_deck_content(project_name="current_project"):
    BASE = Path(f"projects/{project_name}")
    
    print("=== DEBUGGING DECK GENERATION ===")
    
    # Check memo directory
    MEMO = BASE / "memo"
    print(f"Memo directory exists: {MEMO.exists()}")
    if MEMO.exists():
        memo_files = list(MEMO.glob("*.md"))
        print(f"Memo files found: {len(memo_files)}")
        for f in memo_files:
            print(f"  - {f.name}")
            try:
                content = f.read_text(encoding="utf-8")[:100]
                print(f"    Preview: {content}...")
            except:
                print(f"    Error reading")
    
    # Check financial summary
    FINANCIAL = BASE / "financial/summary.json"
    print(f"Financial summary exists: {FINANCIAL.exists()}")
    if FINANCIAL.exists():
        try:
            data = json.loads(FINANCIAL.read_text())
            print(f"Financial data: {data}")
        except:
            print("Error reading financial data")
    
    # Check deck output
    DECK = BASE / "deck/deck.md"
    print(f"Deck file exists: {DECK.exists()}")
    if DECK.exists():
        content = DECK.read_text(encoding="utf-8")
        print(f"Deck content length: {len(content)} chars")
        print(f"First 500 chars:\n{content[:500]}")

if __name__ == "__main__":
    debug_deck_content()