RAG (Retrieval-Augmented Generation)

A simple Retrieval-Augmented Generation (RAG) application that allows users to ask questions about their own documents. The system retrieves relevant information from the documents and uses an LLM to generate accurate, context-aware answers.

🚀 Features
Upload and process documents
Split documents into smaller chunks
Generate embeddings for document chunks
Store embeddings in a vector database
Perform similarity search
Retrieve relevant document context
Generate answers using an LLM
Ask questions using natural language
🏗️ RAG Architecture
Documents
    ↓
Document Loading
    ↓
Text Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Generated Answer
🛠️ Technologies
Python
LangChain / LlamaIndex
LLM API
Embeddings
Vector Database
FastAPI (optional, for creating the backend API)
📂 Project Structure
rag-project/
│
├── documents/
│   └── sample.pdf
│
├── src/
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
⚙️ Installation

Clone the repository:

git clone <your-repository-url>
cd rag-project

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
🔑 Environment Variables

Create a .env file:

OPENAI_API_KEY=your_api_key

Never commit your API key to GitHub.

▶️ Run the Project
python src/main.py

If you later add FastAPI:

uvicorn src.main:app --reload

API documentation will be available at:

http://127.0.0.1:8000/docs
💡 Example

Question:

What is the company's leave policy?

RAG process:

Question
   ↓
Search vector database
   ↓
Retrieve relevant document chunks
   ↓
Send context + question to LLM
   ↓
Generate answer
🎯 Learning Goals

This project helps demonstrate understanding of:

LLMs
Embeddings
Vector databases
Semantic search
Document chunking
Retrieval
Prompt engineering
RAG pipelines
AI application development
🔮 Future Improvements
 Add PDF upload
 Add multiple document support
 Add chat history
 Add source citations
 Add authentication
 Add FastAPI backend
 Add React frontend
 Dockerize the application
 Deploy the application
👨‍💻 Author

Sumit Tiruwa

AI/ML & Backend Developer
