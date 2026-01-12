import os

def create_project(project):
    name = f"{project.type}-{project.sector}-{project.territory}"
    base = f"projects/{name}"

    folders = [
        "raw_docs",
        "standardized/docs",
        "standardized/knowledge/case_studies",
        "standardized/knowledge/regulatory_notes",
        "insights",
        "memo",
        "deck"
    ]

    for f in folders:
        os.makedirs(f"{base}/{f}", exist_ok=True)

    return {
        "project_id": name,
        "status": "created"
    }