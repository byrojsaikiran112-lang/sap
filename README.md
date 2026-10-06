# LearnSphere — GenAI Personalized Learning Assistant

## 1. Project idea
A deployable web-based LMS assistant that accepts student learning requirements and uses a GenAI model to produce personalized study plans, explanations, quizzes, and flashcards.

## 2. Technology stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python FastAPI
- Database: SQLite
- GenAI: Google Gemini API using the `google-genai` Python SDK
- Deployment: Render (or any Python web host)

## 3. Exact execution order

### Step 1 — Install Python
Use Python 3.11+.

### Step 2 — Open terminal
```text
cd ai_lms_project
```

### Step 3 — Create virtual environment
Windows:
```text
python -m venv venv
venv\Scripts\activate
```

### Step 4 — Install dependencies
```text
pip install -r backend/requirements.txt
```

### Step 5 — Configure Gemini API
Create a Gemini API key in Google AI Studio.
Copy `backend/.env.example` to `backend/.env` and put:
```text
GEMINI_API_KEY=YOUR_KEY
GEMINI_MODEL=gemini-3.8-flash
```
Never upload `.env` or expose the API key in frontend JavaScript.

### Step 6 — Run backend
```text
cd backend
uvicorn main:app --reload
```

### Step 7 — Open application
Open:
```text
http://127.0.0.1:8000
```

### Step 8 — Test
Try:
- Course: Data Structures
- Topic: AVL Trees
- Level: Intermediate
- Goal: Prepare for exam
- Mode: Study Plan

Then test Explain, Quiz and Flashcards.

## 4. Architecture
User Input
→ Frontend JavaScript
→ FastAPI `/api/generate`
→ Prompt Construction
→ Gemini API
→ Response Processing
→ SQLite History
→ Frontend Output
→ User Feedback

## 5. API endpoints
GET `/api/health`
POST `/api/generate`
GET `/api/history`
POST `/api/feedback`

## 6. Deployment
For Render:
- Runtime: Python
- Build command: `pip install -r backend/requirements.txt`
- Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `GEMINI_API_KEY`
- Environment variable: `GEMINI_MODEL=gemini-3.8-flash`

## 7. Evaluation
Evaluate output on:
- Relevance to input topic
- Correctness
- Clarity
- Level appropriateness
- Completeness
- Usefulness for exam preparation

Use the built-in 1–5 rating and comments as user feedback evidence.

## 8. Security notes
- Keep the Gemini API key only on the backend.
- Add authentication and rate limiting before large-scale public use.
- Validate all user inputs.
- Do not store sensitive student information unnecessarily.
