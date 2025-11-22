# 🎤 AI Interview Practice Partner  
A conversational AI agent built for the Eightfold Agentic AI Internship assignment.  
This project allows users to practice interviews with a realistic AI interviewer and receive detailed, professional feedback.

---

## 🚀 Features  
- Conducts mock interviews for selected job roles  
- Asks contextual follow-up questions  
- Adapts to user response style (efficient, confused, chatty)  
- Provides detailed structured feedback (strengths, areas to improve, tips, rating)  
- Voice support (optional – but included in frontend design)  
- Fast, free LLM using Groq API (Llama-3 models)

---

## 🛠️ Tech Stack  
### **Backend (Python – FastAPI)**
- FastAPI  
- Groq API (llama-3.1-8b-instant model – FREE)  
- Pydantic  
- Uvicorn  
- dotenv  

### **Frontend**
- HTML  
- CSS  
- JavaScript  
- Browser Speech-to-Text (Web Speech API)  
- Live Server

---

## 📂 Project Structure

```
interview-practice-agent/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

---

# 🔧 **Installation & Setup**

## 1️⃣ Clone the Repository

```
git clone <your-repo-url>
cd interview-practice-agent
```

---

# 🧠 Backend Setup (FastAPI)

## 2️⃣ Create Virtual Environment

```
cd backend
python -m venv venv
venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## 4️⃣ Add Your Groq API Key  
Create a `.env` file inside **backend/**:

```
GROQ_API_KEY=your_key_here
```

Get your free API key: https://console.groq.com/keys  
(No credit card required)

---

## 5️⃣ Run the Backend

```
uvicorn main:app --reload
```

Backend will run at:

👉 **http://127.0.0.1:8000**

Check health:

👉 http://127.0.0.1:8000/health

---

# 💻 Frontend Setup

## 6️⃣ Open the frontend folder

```
cd ../frontend
```

Right-click **index.html** →  
👉 **Open With Live Server**

Or open manually:

👉 http://127.0.0.1:5500/frontend/index.html

---

# 🧪 How to Use  
1. Select job role, experience level, and mode  
2. Click **Start Interview**  
3. Answer questions (text or voice)  
4. AI interviewer asks smart follow-ups  
5. Click **Get Feedback**  
6. Receive:
   - Strengths  
   - Areas to improve  
   - Actionable tips  
   - Rating (0–5)

---

# 📌 Architecture Overview

```
Frontend (HTML/JS) 
     ↓ REST API calls (fetch)
Backend (FastAPI)
     ↓
Groq LLM (Llama 3.1 Models)
```

- Frontend sends `/start`, `/message`, `/finish`
- Backend stores session → generates next question
- Feedback is created using structured prompt engineering

---

# 🤖 Design Decisions

### 1. **Why Groq Llama-3.1?**
- Fastest free inference  
- No quota issues  
- Great for conversational tasks  

### 2. **Why FastAPI?**
- Lightweight  
- Easy routing  
- Async for smooth processing  

### 3. **Why Web Speech API for Voice?**
- No external dependency  
- Works in browser  
- Simple to integrate  

### 4. **Stateful Sessions**
Used in-memory dictionary:
```
SESSIONS = { sessionId: { role, level, mode, qa[] } }
```

---

# 🎥 Demo Instructions (for submission)

Your demo video (max 10 minutes) should show:

### ✔ Starting backend  
### ✔ Running frontend  
### ✔ Multiple interview styles:
- Efficient user  
- Chatty user  
- Confused user  
- Off-topic user  

### ✔ Getting feedback  
### ✔ Explain architecture & design choices  

No slides needed — only screen recording with voice.

---

# ✅ This meets all Eightfold Assignment Requirements

- Conversational quality  
- Agentic behaviour  
- Multi-persona handling  
- Technical implementation  
- Natural interaction  
- Detailed README  
- Clear architecture reasoning  

---

# 🙌 Author  
**Modi Sireesha**  
Eightfold Agentic AI Internship – Assignment Submission

