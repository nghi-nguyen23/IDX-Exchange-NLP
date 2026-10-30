import time
import numpy as np
import faiss


embeddings = np.load(
    "data/processed/week5_embeddings.npy"
).astype("float32")

embeddings_10k = np.tile(
    embeddings,
    (10, 1)
)[:10000]

index = faiss.IndexFlatIP(
    embeddings_10k.shape[1]
)

index.add(embeddings_10k)

query_embedding = embeddings_10k[0:1]

start = time.perf_counter()

scores, indices = index.search(
    query_embedding,
    5
)

end = time.perf_counter()

latency_ms = (end - start) * 1000

print(f"Listings indexed: {index.ntotal}")
print(f"10k FAISS search latency: {latency_ms:.2f} ms")