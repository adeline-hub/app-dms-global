import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from utils.rag import search
from utils.llm import ask

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args()
    
    # ✅ RAG SEARCH (project‑scoped)
    chunks = search(
        query=args.question,
        project=args.project
    )

    context = "\n\n".join(
        f"Source: {src}\n{txt}" for txt, src in chunks
    )

    answer = ask(f"""
    You are a professional investment analyst.

    Answer the question using ONLY the context below.
    Cite sources explicitly.

    Context:
    {context}

    Question:
    {args.question}
    """)

    print("\nANSWER:\n")
    print(answer)

if __name__ == "__main__":
    main()