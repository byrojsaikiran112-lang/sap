# LearnSphere — GenAI Personalized Learning Assistant

## Abstract
LearnSphere is a web-based personalized learning management application that integrates Generative AI into the student learning workflow. A student enters a subject, topic, academic level, learning goal and available study time. The system constructs a controlled prompt and sends it to the Gemini GenAI API. The generated response is processed by the FastAPI backend, saved in SQLite for learning history, and displayed through an intuitive browser interface. The system supports study-plan generation, topic explanation, quiz generation and flashcard generation.

## 1. Objectives
1. Build a functional, deployable application.
2. Select an appropriate GenAI model/API.
3. Design effective prompts and inputs.
4. Deliver an intuitive user interface.
5. Evaluate output quality.

## 2. Problem Statement
Students often use generic learning resources that do not match their current level, available time or examination goals. The proposed system provides personalized AI-generated learning material from structured student inputs.

## 3. Proposed System / Methodology
1. User Input
2. Prompt Construction
3. GenAI Model API Call
4. Response Processing
5. Output Display
6. Output Quality Evaluation

## 4. Functional Modules
### Student Input Module
Collects name, course, topic, level, goal and study time.

### Prompt Construction Module
Converts structured input into an instruction containing learner context, task requirements and quality constraints.

### GenAI Module
Calls Google Gemini through the official Python SDK.

### Response Processing Module
Checks that a response was returned, stores it in SQLite and sends it to the browser.

### Learning Content Module
Provides:
- Personalized study plan
- Topic explanation
- 10-question quiz
- 12 flashcards

### History Module
Stores recent generated content for review.

### Evaluation Module
Collects 1–5 ratings and optional comments.

## 5. Model Selection
The project uses Gemini 3.8 Flash through the Gemini API. It is selected because the application needs fast text generation and structured educational content. The current Gemini documentation shows Python usage through `google-genai` and `client.models.generate_content`. Model availability and naming can change, so the model name is kept in an environment variable.

## 6. Prompt Design
The prompt contains:
- Role: expert college learning assistant
- Student profile: level, course, topic
- Constraints: accuracy, clarity and difficulty matching
- Goal and available study time
- Task-specific output requirements

This is better than sending only the topic because the model receives context about the learner and desired result.

## 7. System Architecture
Browser Frontend
    ↓
FastAPI REST Backend
    ↓
Prompt Builder
    ↓
Gemini API
    ↓
Response
    ↓
SQLite + Browser

## 8. Database Design
Table: generations
- id
- student_name
- course
- topic
- level
- mode
- output
- created_at

Table: feedback
- id
- generation_id
- rating
- comment
- created_at

## 9. Input → Processing → Output Example
Input:
Course = Data Structures
Topic = AVL Trees
Level = Intermediate
Goal = Exam preparation
Study Time = 60 minutes

Processing:
The backend creates a study-plan prompt and sends it to Gemini.

Output:
The student receives learning objectives, prerequisites, time-boxed study steps, practice tasks, self-assessment and exam tips.

## 10. Evaluation Method
A five-point Likert-style rating can be used:
1 = Very poor
2 = Poor
3 = Average
4 = Good
5 = Excellent

Quality criteria:
- Relevance
- Correctness
- Clarity
- Completeness
- Personalization
- Practical usefulness

For the final report, test at least 10 prompts across different subjects and record the average rating.

## 11. Test Cases
TC01: Valid study-plan request → content generated.
TC02: Valid explanation request → explanation generated.
TC03: Quiz request → 10 questions generated.
TC04: Flashcard request → 12 flashcards generated.
TC05: Empty topic → frontend validation prevents submission.
TC06: Invalid mode → backend returns HTTP 400.
TC07: Missing API key → clear backend error.
TC08: History request → previous generations displayed.
TC09: Feedback submission → rating stored.
TC10: Health check → API returns status OK.

## 12. Advantages
- Personalized learning
- Multiple learning formats
- Fast content generation
- Learning history
- Built-in quality feedback
- Simple and deployable architecture
- API key protected on backend

## 13. Limitations
- GenAI can occasionally produce incorrect information.
- Internet/API access is required.
- API usage may have quotas or costs.
- Current version does not include full user authentication, course enrollment, teacher dashboards or formal grading.

## 14. Future Enhancements
- Student and teacher login
- Course enrollment
- Teacher-created course material
- PDF/document upload and RAG
- Progress tracking
- Automatic quiz scoring
- Student performance analytics
- Admin dashboard
- Email notifications
- Role-based access control

## 15. Conclusion
LearnSphere demonstrates how Generative AI can be integrated into a practical educational application. It follows a complete pipeline from user input to prompt construction, model API call, response processing, display and quality evaluation. The architecture separates frontend, backend, AI service and database responsibilities, making the project suitable for academic demonstration and further deployment.

## 16. Viva Explanation — 60 seconds
"My project is LearnSphere, a GenAI personalized learning management system. The student enters the subject, topic, academic level, learning goal and study time. The frontend sends this information to a FastAPI backend. The backend constructs a structured prompt and calls the Gemini API. The response is processed and stored in SQLite and then displayed to the student. The system can generate personalized study plans, topic explanations, quizzes and flashcards. I also included learning history and a 1-to-5 feedback mechanism to evaluate output quality. The main objective is to demonstrate a complete deployable GenAI application rather than only an AI chatbot."
