from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from app.rag.loader import PDFLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import VectorStore

router = APIRouter()

# Initialize components
vectorstore = VectorStore()

# Document directory
DOCUMENTS_DIR = "documents"
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and index a PDF document"""
    
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save file
        file_path = os.path.join(DOCUMENTS_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Load and process
        loader = PDFLoader(DOCUMENTS_DIR)
        documents = loader.load_pdf(file_path)
        
        # Split documents
        splitter = TextSplitter(chunk_size=500, overlap=100)
        chunks = splitter.split_documents(documents)
        
        # Add to vector store
        vectorstore.add_documents(chunks)
        
        return {
            "message": f"Document '{file.filename}' uploaded successfully",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "total_documents": vectorstore.get_size()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents():
    """List all indexed documents"""
    
    try:
        documents = os.listdir(DOCUMENTS_DIR)
        pdf_files = [f for f in documents if f.endswith('.pdf')]
        
        return {
            "total_files": len(pdf_files),
            "files": pdf_files,
            "total_chunks": vectorstore.get_size()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear")
async def clear_documents():
    """Clear all indexed documents"""
    
    try:
        # Clear vector store
        vectorstore.clear()
        
        # Clear documents directory
        if os.path.exists(DOCUMENTS_DIR):
            shutil.rmtree(DOCUMENTS_DIR)
            os.makedirs(DOCUMENTS_DIR, exist_ok=True)
        
        return {
            "message": "All documents cleared successfully",
            "total_chunks": 0
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index-all")
async def index_all_documents():
    """Index all PDF documents in the documents folder"""
    
    try:
        loader = PDFLoader(DOCUMENTS_DIR)
        all_documents = loader.load_all_documents()
        
        if not all_documents:
            raise HTTPException(status_code=400, detail="No PDF documents found")
        
        # Split documents
        splitter = TextSplitter(chunk_size=500, overlap=100)
        chunks = splitter.split_documents(all_documents)
        
        # Add to vector store
        vectorstore.add_documents(chunks)
        
        return {
            "message": "All documents indexed successfully",
            "documents_indexed": len(all_documents),
            "total_chunks": len(chunks),
            "vector_store_size": vectorstore.get_size()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
