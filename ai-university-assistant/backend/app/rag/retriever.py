from typing import List, Dict
from app.rag.vectorstore import VectorStore

class Retriever:
    """Retrieve relevant documents based on query"""
    
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore
    
    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        """Retrieve top-k relevant documents"""
        return self.vectorstore.search(query, k)
    
    def format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents as context string"""
        context = ""
        
        for idx, doc in enumerate(documents, 1):
            context += f"\n--- Document {idx} ---\n"
            context += f"Source: {doc.get('source', 'Unknown')}\n"
            context += f"Page: {doc.get('page', 'N/A')}\n"
            context += f"Content: {doc.get('content', '')}\n"
        
        return context
    
    def get_sources(self, documents: List[Dict]) -> str:
        """Format sources information"""
        sources = ""
        seen = set()
        
        for doc in documents:
            source_key = (doc.get('source'), doc.get('page'))
            if source_key not in seen:
                sources += f"• {doc.get('source', 'Unknown')} (Page {doc.get('page', 'N/A')})\n"
                seen.add(source_key)
        
        return sources
