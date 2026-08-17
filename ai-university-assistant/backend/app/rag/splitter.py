from typing import List, Dict

class TextSplitter:
    """Split text into overlapping chunks"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.overlap
        
        return chunks
    
    def split_documents(self, documents: List[Dict]) -> List[Dict]:
        """Split document list into chunks while preserving metadata"""
        chunked_docs = []
        
        for doc in documents:
            content = doc.get("content", "")
            chunks = self.split_text(content)
            
            for chunk_idx, chunk in enumerate(chunks):
                chunked_docs.append({
                    "content": chunk,
                    "source": doc.get("source"),
                    "page": doc.get("page"),
                    "chunk_id": chunk_idx,
                    "metadata": doc.get("metadata")
                })
        
        return chunked_docs
