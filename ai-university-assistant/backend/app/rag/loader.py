import os
from pathlib import Path
from PyPDF2 import PdfReader
from typing import List, Dict

class PDFLoader:
    """Load and extract text from PDF documents"""
    
    def __init__(self, document_dir: str = "documents"):
        self.document_dir = document_dir
        self.documents = []
    
    def load_pdf(self, file_path: str) -> List[Dict]:
        """
        Load a single PDF file and extract text
        Returns list of documents with metadata
        """
        documents = []
        
        try:
            pdf_reader = PdfReader(file_path)
            file_name = Path(file_path).name
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                
                if text.strip():
                    documents.append({
                        "content": text,
                        "source": file_name,
                        "page": page_num + 1,
                        "metadata": {
                            "source": file_name,
                            "page": page_num + 1
                        }
                    })
        
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
        
        return documents
    
    def load_all_documents(self) -> List[Dict]:
        """Load all PDF documents from directory"""
        all_documents = []
        
        pdf_dir = Path(self.document_dir)
        if not pdf_dir.exists():
            pdf_dir.mkdir(parents=True, exist_ok=True)
        
        for pdf_file in pdf_dir.glob("*.pdf"):
            print(f"Loading {pdf_file.name}...")
            docs = self.load_pdf(str(pdf_file))
            all_documents.extend(docs)
        
        self.documents = all_documents
        return all_documents
    
    def get_documents_count(self) -> int:
        """Get total number of loaded documents"""
        return len(self.documents)
