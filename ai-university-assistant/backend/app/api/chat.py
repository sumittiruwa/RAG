from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.rag.vectorstore import VectorStore
from app.rag.retriever import Retriever
from app.llm.generator import AnswerGenerator
from app.ml.classifier import IntentClassifier

router = APIRouter()

# Initialize components
vectorstore = VectorStore()
retriever = Retriever(vectorstore)
generator = AnswerGenerator()
classifier = IntentClassifier()

# Pydantic models
class MessageRequest(BaseModel):
    message: str
    history: List[Dict] = []

class MessageResponse(BaseModel):
    answer: str
    sources: str
    intent: str
    confidence: float

# Chat endpoint
@router.post("/ask", response_model=MessageResponse)
async def ask_question(request: MessageRequest):
    """Ask a question to the university assistant"""
    
    try:
        question = request.message.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Classify intent
        intent, confidence = classifier.predict(question)
        
        # Retrieve relevant documents
        documents = retriever.retrieve(question, k=3)
        
        if not documents:
            return MessageResponse(
                answer="I couldn't find relevant information about this topic. Please check the uploaded documents or ask another question.",
                sources="No sources found",
                intent=intent,
                confidence=confidence
            )
        
        # Format context
        context = retriever.format_context(documents)
        
        # Generate answer
        answer = generator.generate_answer(question, context)
        
        # Get sources
        sources = retriever.get_sources(documents)
        
        return MessageResponse(
            answer=answer,
            sources=sources,
            intent=intent,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get statistics
@router.get("/stats")
async def get_stats():
    """Get chatbot statistics"""
    return {
        "documents_indexed": vectorstore.get_size(),
        "intents": classifier.INTENTS
    }
