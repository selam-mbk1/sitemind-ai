import faiss
import numpy as np

dimension = 1024
index = faiss.IndexFlatL2(dimension)

def add_embedding(embedding):
    vector = np.array([embedding]).astype("float32")
    index.add(vector)
    return index.ntotal - 1

def search(query_embedding, k=5):
    vector = np.array([query_embedding]).astype("float32")
    D, I = index.search(vector, k)
    return I[0]

