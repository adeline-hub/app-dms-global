from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pickle

BASE = Path("projects/business-food-chad/standardized/docs")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts, sources = [], []

for doc in BASE.glob("*.md"):
    text = doc.read_text(encoding="utf-8")
    texts.append(text)
    sources.append(doc.name)

embeddings = model.encode(texts)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

pickle.dump((index, texts, sources), open("rag_index.pkl", "wb"))
print("RAG index built")