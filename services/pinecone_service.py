import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

class PineconeService:
    def __init__(self):
        self.pinecone = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.index_name = "flashcard-embeddings-v1"

    def search_similar(self, embeds):
        return self.pinecone.Index(self.index_name).query(
            vector=[embeds], top_k=5, include_metadata=True
        )

    def insert(self, embeds):
        return self.pinecone.Index(self.index_name).upsert(vectors=embeds)
