# 🎓 AI University Assistant

An intelligent chatbot system that helps university students find information about courses, attendance, exams, and more using RAG (Retrieval-Augmented Generation).

## 📋 Features

✅ **RAG-based Answer Generation** - Uses university documents for accurate answers
✅ **PDF Document Processing** - Automatically indexes university PDFs
✅ **Semantic Search** - Finds relevant information using embeddings
✅ **Intent Classification** - Categorizes student questions
✅ **Source Citation** - Shows document sources for verification
✅ **Multi-channel Integration** - Works with LLMs via GROQ API
✅ **Real-time Chat** - WebSocket support for live conversations
✅ **Beautiful UI** - Modern React frontend with intuitive design

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│            Frontend (React + Vite)              │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│         Backend (FastAPI + Python)              │
│  ┌──────────────────────────────────────────┐  │
│  │  RAG Pipeline                            │  │
│  │  ├─ PDF Loader                           │  │
│  │  ├─ Text Splitter                        │  │
│  │  ├─ Sentence Transformers               │  │
│  │  ├─ FAISS Vector Database                │  │
│  │  ├─ LLM (GROQ)                          │  │
│  │  └─ Intent Classifier                   │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### 1. Clone & Setup

```bash
cd ai-university-assistant
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Environment is already configured with GROQ API key in .env

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

### 4. Upload Documents

1. Open the frontend at `http://localhost:5173`
2. Use the sidebar to upload PDF documents
3. Ask questions about your university information

## 📁 Project Structure

```
ai-university-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── api/
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── documents.py     # Document upload
│   │   │   └── auth.py          # Authentication
│   │   ├── rag/
│   │   │   ├── loader.py        # PDF loader
│   │   │   ├── splitter.py      # Text chunking
│   │   │   ├── embeddings.py    # Vector generation
│   │   │   ├── vectorstore.py   # FAISS index
│   │   │   └── retriever.py     # Document retrieval
│   │   ├── llm/
│   │   │   └── generator.py     # LLM answer generation
│   │   └── ml/
│   │       └── classifier.py    # Intent classification
│   ├── .env                      # Environment variables
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main App component
│   │   ├── App.css              # App styles
│   │   ├── main.jsx             # React entry point
│   │   ├── index.css            # Global styles
│   │   └── components/
│   │       ├── ChatWindow.jsx   # Chat display
│   │       ├── DocumentUpload.jsx # Upload UI
│   │       └── Sidebar.jsx       # Sidebar navigation
│   ├── index.html               # HTML entry point
│   ├── package.json             # Node dependencies
│   ├── vite.config.js           # Vite configuration
│   └── .gitignore               # Git ignore rules
│
├── documents/                    # PDF files to index
├── ml_dataset/
│   └── intents.csv              # Training data
├── vectorstore/                  # FAISS indices
└── README.md                     # This file
```

## 🔑 Environment Variables

**Backend (.env)**
```env
GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

The GROQ API key is already configured in `.env`.

## 📚 How It Works

### Document Processing
1. Upload PDF documents through the web interface
2. `PDFLoader` extracts text from each page
3. `TextSplitter` breaks text into manageable chunks
4. `EmbeddingGenerator` converts chunks to vectors using Sentence Transformers
5. `VectorStore` (FAISS) indexes vectors for fast retrieval

### Query Processing
1. User asks a question in the chat
2. `IntentClassifier` identifies question type
3. Question is converted to vector embedding
4. `FAISS` searches for similar document chunks
5. `Retriever` formats context from top results
6. `AnswerGenerator` (GROQ LLM) creates natural-language answer
7. Response includes answer + sources + metadata

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Fast, async Python web framework
- **PyPDF2** - PDF text extraction
- **Sentence Transformers** - Text embeddings
- **FAISS** - Vector database for similarity search
- **Groq** - LLM API for answer generation
- **Scikit-learn** - ML models for classification

### Frontend
- **React** - UI library
- **Vite** - Fast build tool
- **Axios** - HTTP client
- **CSS3** - Styling

## 📖 API Endpoints

### Chat
- `POST /api/chat/ask` - Ask a question
- `GET /api/chat/stats` - Get system statistics

### Documents
- `POST /api/documents/upload` - Upload PDF
- `GET /api/documents/list` - List indexed documents
- `POST /api/documents/index-all` - Index all PDFs
- `DELETE /api/documents/clear` - Clear all documents

### Auth
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

## 🎯 Example Usage

### Upload Sample Document

1. Create a PDF document with university information
2. Click "Upload Documents" in sidebar
3. Select PDF files
4. Click "Upload"

### Ask Questions

```
"What is the attendance requirement?"
"When is the exam?"
"What subjects are in BCA?"
"What are admission requirements?"
```

## ⚙️ Configuration

### Chunk Size
Edit in `backend/app/config.py`:
```python
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Overlap between chunks
```

### Retrieval Parameters
```python
TOP_K_RETRIEVAL = 3  # Number of results to return
```

### LLM Model
Edit in `backend/app/llm/generator.py`:
```python
self.model = "mixtral-8x7b-32768"  # Groq model
```

## 🚨 Troubleshooting

### Backend not connecting
```bash
# Check if FastAPI is running
curl http://localhost:8000/health

# Restart backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### GROQ API Key error
```bash
# Check .env file
cat backend/.env

# Ensure GROQ_API_KEY is set correctly
GROQ_API_KEY=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
```

### No documents indexed
1. Upload PDFs through UI
2. Check `/api/documents/list` endpoint
3. Verify files in `documents/` folder

## 📈 Performance Tips

- Use smaller PDFs for better performance
- Adjust CHUNK_SIZE based on document structure
- Increase TOP_K_RETRIEVAL for more thorough search
- Monitor FAISS index size

## 🔒 Security

- Change `SECRET_KEY` in `.env` for production
- Implement proper authentication
- Validate all file uploads
- Use HTTPS in production

## 📝 Example Intents

The classifier recognizes these question types:
- **Attendance** - About attendance requirements
- **Examination** - About exams and dates
- **Course** - About course structure
- **Admission** - About admission process
- **Fee** - About fees and payments
- **Other** - General questions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues and questions:
- Check existing documentation
- Review API responses for error details
- Check console logs in browser dev tools
- Review server logs in terminal

---

**Built with ❤️ using FastAPI & React**

Version: 1.0.0
Last Updated: 2024
