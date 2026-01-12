import subprocess

def run(project_id: str):
    steps = [
        ("standardize_documents.py",),
        ("extract_key_insights.py",),
        ("generate_draft_memo_sections.py",),
        ("generate_structure_overview.py",)
    ]

    for (script,) in steps:
        subprocess.run(
            ["python", f"scripts/{script}", "--project", project_id],
            check=True
        )

    return {"status": "pipeline_completed"}