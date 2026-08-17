# ⚡ Quick Start Guide

## 🎯 Get Running in 5 Minutes!

### Step 1: Terminal 1 - Start Backend

```bash
# Navigate to backend
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
python -m uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Terminal 2 - Start Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start dev server
npm run dev
```

**Expected output:**
```
➜  Local:   http://localhost:5173/
```

### Step 3: Open Browser

Go to: **http://localhost:5173**

🎉 **You're in!**

---

## 🚀 Ready to Use

### 1️⃣ Upload PDF
- Click **"📤 Upload Documents"** in sidebar
- Select your PDF files
- Click upload button

### 2️⃣ Ask Questions
Type in chat box:
```
What is the attendance requirement?
When is the exam?
What subjects are in the course?
```

### 3️⃣ Get Answers
- AI generates answer from your documents
- Shows source references
- Displays question intent & confidence

---

## 🔗 Important URLs

| Purpose | URL |
|---------|-----|
| Chat Application | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| API Health Check | http://localhost:8000/health |

---

## 📋 Default Test Credentials

**Login (if needed):**
- Username: `student`
- Password: `password123`

Or:
- Username: `admin`
- Password: `admin123`

---

## 🆘 Quick Fixes

### Backend not starting?
```bash
# Change port
python -m uvicorn app.main:app --port 8001
```

### Frontend not installing?
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### Can't find localhost:5173?
Check terminal output - the exact URL is shown there

---

## 📚 Sample Questions to Test

Once you upload PDFs with university info:

- ✅ "What is the minimum attendance?"
- ✅ "When will exams start?"
- ✅ "What are the required courses?"
- ✅ "How do I apply for admission?"
- ✅ "What is the fee structure?"
- ✅ "What are the college rules?"

---

## 🎓 Next Steps

1. **Read SETUP.md** - Detailed installation guide
2. **Check README.md** - Full documentation
3. **Upload documents** - Add your PDF files
4. **Customize** - Modify prompts in backend code

---

**Need help? Check the logs in your terminal! 🔍**
