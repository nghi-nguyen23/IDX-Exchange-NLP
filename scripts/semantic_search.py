from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SemanticSearcher:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.listings = None

    def build_index(self, remarks_list):
        print(f"Encoding {len(remarks_list)} listings...")

        embeddings = self.model.encode(
            remarks_list,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        self.listings = remarks_list

        return embeddings

    def search(self, query, k=5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for i, index in enumerate(indices[0]):
            results.append({
                "remark": self.listings[index],
                "distance": float(distances[0][i])
            })

        return results