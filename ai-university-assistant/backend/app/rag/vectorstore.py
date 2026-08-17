import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple
from app.rag.embeddings import EmbeddingGenerator

class VectorStore:
    """FAISS-based vector database for document storage and retrieval"""
    
    def __init__(self, index_path: str = "vectorstore/faiss_index.bin", 
                 metadata_path: str = "vectorstore/metadata.pkl"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_generator = EmbeddingGenerator()
        self.index = None
        self.metadata = []
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Try to load existing index
        self.load()
    
    def add_documents(self, documents: List[Dict]) -> None:
        """Add documents to vector store"""
        texts = [doc["content"] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedding_generator.embed_texts(texts)
        embeddings = embeddings.astype('float32')
        
        # Create index if not exists
        if self.index is None:
            embedding_dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(embedding_dim)
        
        # Add vectors
        self.index.add(embeddings)
        
        # Store metadata
        for doc in documents:
            self.metadata.append({
                "content": doc["content"],
                "source": doc.get("source"),
                "page": doc.get("page"),
                "chunk_id": doc.get("chunk_id", 0)
            })
        
        # Save
        self.save()
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        if self.index is None or len(self.metadata) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_generator.embed_text(query)
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, min(k, len(self.metadata)))
        
        # Return results
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append({
                    **self.metadata[idx],
                    "distance": float(distances[0][len(results)])
                })
        
        return results
    
    def save(self) -> None:
        """Save index and metadata"""
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load(self) -> None:
        """Load existing index and metadata"""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, 'rb') as f:
                    self.metadata = pickle.load(f)
            except:
                pass
    
    def clear(self) -> None:
        """Clear vector store"""
        self.index = None
        self.metadata = []
        
        # Remove files
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.metadata_path):
            os.remove(self.metadata_path)
    
    def get_size(self) -> int:
        """Get number of documents in store"""
        return len(self.metadata)
