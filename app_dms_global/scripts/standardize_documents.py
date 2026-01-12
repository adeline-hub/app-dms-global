import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from pypdf import PdfReader
from docx import Document

def standardize_documents(project_name):  # <-- Function takes parameter
    BASE = Path(f"projects/{project_name}")
    RAW = BASE / "raw_docs"
    OUT = BASE / "standardized/docs"
    OUT.mkdir(parents=True, exist_ok=True)

    SUPPORTED = {".pdf", ".docx"}

    def extract_text(file: Path) -> str:
        if file.suffix.lower() == ".pdf":
            reader = PdfReader(file)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        if file.suffix.lower() == ".docx":
            doc = Document(file)
            return "\n".join(p.text for p in doc.paragraphs)

        return ""

    for file in RAW.iterdir():
        if file.suffix.lower() not in SUPPORTED:
            print(f"Skipping unsupported file: {file.name}")
            continue

        text = extract_text(file)
        if not text.strip():
            print(f"No text extracted from: {file.name}")
            continue

        out = OUT / f"{file.stem}.md"
        out.write_text(
            f"# Source: {file.name}\n\n{text}",
            encoding="utf-8"
        )

    print("Documents extracted & standardized")
    return True  # <-- Optional: return success status

def main():  # <-- Separate main function for CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    args = parser.parse_args()
    
    standardize_documents(args.project)  # <-- Call function with argument
    
if __name__ == "__main__":
    main()  # <-- Only runs when script is executed directly