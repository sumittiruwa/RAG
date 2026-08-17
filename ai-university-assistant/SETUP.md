# 🚀 AI University Assistant - Setup Guide

## Prerequisites

Ensure you have the following installed:
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** (optional) - [Download](https://git-scm.com/)

## Step-by-Step Installation

### Step 1: Extract Project

Extract the `ai-university-assistant.zip` file to your desired location.

```bash
unzip ai-university-assistant.zip
cd ai-university-assistant
```

### Step 2: Backend Setup

#### 2.1 Navigate to backend directory
```bash
cd backend
```

#### 2.2 Create Python virtual environment (recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Python dependencies
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn
- PyPDF2 for PDF processing
- Sentence Transformers
- FAISS for vector search
- Groq SDK
- And other dependencies

#### 2.4 Verify .env file

The `.env` file is already configured with the GROQ API key:
```env
GROQ_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key-change-this-in-production
ENVIRONMENT=development
```

#### 2.5 Run backend server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**✓ Backend is ready!** Access API docs at `http://localhost:8000/docs`

---

### Step 3: Frontend Setup

**In a new terminal window:**

#### 3.1 Navigate to frontend directory
```bash
cd frontend
```

#### 3.2 Install Node dependencies
```bash
npm install
```

This will install React, Vite, Axios, and other dependencies.

#### 3.3 Start development server
```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**✓ Frontend is ready!** Open `http://localhost:5173` in your browser.

---

## 🎯 First Use

### 1. Open Application

Open your browser and go to: `http://localhost:5173`

You should see the AI University Assistant interface with:
- Chat window in the center
- Sidebar on the left with document upload

### 2. Upload Sample Document

Create a PDF document with university information. For testing, you can create a simple PDF with:
- Attendance requirements
- Exam dates
- Course information
- Admission details

#### Ways to create test PDF:
- Use Microsoft Word → Save as PDF
- Use Google Docs → Download as PDF
- Use online PDF creator
- Use sample documents if provided

### 3. Upload to System

1. Click **"📤 Upload Documents"** in the sidebar
2. Select your PDF file(s)
3. Click **"📤 Upload Documents"** button
4. Wait for confirmation

### 4. Ask Questions

Once documents are uploaded:
1. Type a question in the chat input
2. Press Enter or click send button
3. View the AI-generated answer with sources

#### Example Questions:
- "What is the attendance requirement?"
- "When is the examination?"
- "What subjects are in the course?"
- "What are admission requirements?"

---

## 🔧 Troubleshooting

### Issue: Backend not starting

**Error:** `Address already in use`
```bash
# Kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Then restart:
python -m uvicorn app.main:app --reload --port 8001
```

### Issue: GROQ API Key not working

1. Check `.env` file in backend folder
GROQ_API_KEY=your_api_key_here
3. No spaces before/after the key

### Issue: Frontend can't connect to backend

1. Ensure backend is running on port 8000
2. Check browser console for errors (F12)
3. Verify API endpoint in `frontend/src/App.jsx`: `http://localhost:8000/api`

### Issue: No documents indexed

1. Check if documents are uploaded (check `/documents` folder)
2. Verify upload was successful (check browser console)
3. Refresh page and try again

### Issue: Slow responses from LLM

- This is normal for first requests as models load
- Subsequent requests will be faster
- Check internet connection

---

## 📊 Project Structure After Installation

```
ai-university-assistant/
├── backend/
│   ├── app/                      # Python application
│   ├── venv/                     # Virtual environment (created)
│   ├── .env                      # Environment (with API key)
│   ├── requirements.txt          # Dependencies
│   └── ...
├── frontend/
│   ├── src/                      # React source
│   ├── node_modules/             # Packages (created)
│   ├── package.json              # Dependencies
│   ├── vite.config.js           # Vite config
│   └── ...
├── documents/                    # Upload PDFs here
├── vectorstore/                  # FAISS indices (auto-created)
├── ml_dataset/                   # ML data
├── README.md                     # Main documentation
└── SETUP.md                      # This file
```

---

## 🌐 Accessing the Application

### Local Development

| Component | URL | Port |
|-----------|-----|------|
| Frontend | http://localhost:5173 | 5173 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |

### Testing Endpoints

Open a new terminal and test the API:

```bash
# Health check
curl http://localhost:8000/health

# Get stats
curl http://localhost:8000/api/chat/stats

# Ask a question (requires documents)
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"message":"What is the attendance requirement?"}'
```

---

## 📚 Next Steps

1. **Upload Documents** - Add your university PDFs
2. **Test Questions** - Try asking various questions
3. **Customize** - Modify prompts and configurations
4. **Deploy** - Follow deployment guides for production

## 🔒 Production Deployment

Before deploying to production:

1. **Change SECRET_KEY** in `.env`
```bash
# Generate a new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Update ENVIRONMENT**
```env
ENVIRONMENT=production
```

3. **Setup HTTPS**
4. **Configure CORS** properly
5. **Use a production database**
6. **Setup proper authentication**

---

## 📝 Common Commands

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run server
python -m uvicorn app.main:app --reload

# Run on different port
python -m uvicorn app.main:app --port 8001

# Deactivate virtual environment
deactivate
```

### Frontend

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] GROQ API key configured
- [ ] Can access http://localhost:5173
- [ ] Can upload PDF documents
- [ ] Can ask questions and get answers

---

## 🆘 Getting Help

1. **Check README.md** for overview
2. **Check logs** - Look at terminal output
3. **Browser Console** - Press F12 in browser
4. **API Documentation** - http://localhost:8000/docs

---

**Happy using AI University Assistant! 🎓**
