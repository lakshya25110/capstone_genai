import chromadb
from chromadb.utils import embedding_functions
import os

class RAGService:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="startup_trends",
            embedding_function=self.embedding_fn
        )

    def seed_data(self):
        # Pre-seed with some dummy startup wisdom if empty
        if self.collection.count() == 0:
            docs = [
                "Product-market fit means being in a good market with a product that can satisfy that market. You can always feel when product-market fit isn't happening.",
                "SaaS growth is typically measured by MRR (Monthly Recurring Revenue) and Churn rate. A good monthly growth rate is 5-7%.",
                "Fundraising strategy: Focus on your traction, your team, and your market size. Pitch to investors who have funded similar but non-competing startups.",
                "Hiring for startups: The first 10 employees determine the culture. Hire people who are versatile and can wear multiple hats.",
                "Marketing: Focus on one or two channels that work rather than spreading yourself too thin. Content marketing and SEO are high-leverage for long-term growth."
            ]
            self.add_data(
                documents=docs,
                metadatas=[{"source": "startup_wisdom"} for _ in docs],
                ids=[f"id_{i}" for i in range(len(docs))]
            )

    def add_data(self, documents: list, metadatas: list, ids: list):
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results=3):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results['documents'][0]

    def search(self, query: str):
        return self.query(query, n_results=3)

# Singleton instance
rag_service = RAGService()
rag_service.seed_data()
