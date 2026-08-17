import os
from groq import Groq
from typing import Dict

class AnswerGenerator:
    """Generate answers using Groq LLM"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "mixtral-8x7b-32768"  # Groq's fast model
    
    def generate_answer(self, question: str, context: str) -> str:
        """Generate answer based on question and context"""
        
        prompt = f"""You are a helpful university assistant. Answer the student's question based on the provided university information.

Question: {question}

University Information:
{context}

Instructions:
- Answer based only on the provided university information
- Be concise and clear
- If the information is not available in the provided context, say so
- Use simple, student-friendly language"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I apologize, but I couldn't generate an answer at this moment. Please try again later."
    
    def generate_short_answer(self, question: str, context: str) -> str:
        """Generate shorter answer"""
        
        prompt = f"""You are a university assistant. Answer briefly.

Question: {question}
Context: {context}

Provide a concise answer in 2-3 sentences."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "I couldn't generate an answer."
