import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import argparse
from utils.llm import ask

def project_reasoning(question):  # <-- Function takes parameter
    answer = ask(question)
    return answer  # <-- Return the answer instead of printing

def main():  # <-- Separate main function for CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args()

    answer = project_reasoning(args.question)  # <-- Call function with argument
    print("\nANSWER:\n", answer)
    
if __name__ == "__main__":
    main()  # <-- Only runs when script is executed directly