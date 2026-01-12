from pathlib import Path
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_index(project):
    index_path = Path(f"projects/{project}/rag/index.pkl")
    return pickle.load(open(index_path, "rb"))

def search(query, project, k=3):
    index, texts, sources = load_index(project)
    emb = model.encode([query])
    _, ids = index.search(emb, k)
    return [(texts[i], sources[i]) for i in ids[0]]