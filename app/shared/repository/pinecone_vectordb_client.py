import pinecone
from sentence_transformers import SentenceTransformer

from app.infra.config import settings
from app.shared.domain.repository.vectordb_client import VectorDBClient

transformer_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')


class PineconeVectorDBClient(VectorDBClient):

    def __init__(self):
        self._index = pinecone.Index(settings.PINECONE_INDEX_NAME)
    
    def upsert(self, id: str, data: str, metadata: dict):
        embedding = transformer_model.encode(data).tolist()
        self._index.upsert([(id, embedding, metadata)])
        return "record created"

    def query(self, query: str):
        embedding = transformer_model.encode(query).tolist()
        result = self._index.query(embedding, top_k=100, include_metadata=True)
        return result
        # return []
