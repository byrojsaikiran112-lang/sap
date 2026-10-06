def build_prompt(data):
    student = data["student_name"].strip()
    course = data["course"].strip()
    topic = data["topic"].strip()
    level = data["level"]
    mode = data["mode"]
    goal = data.get("goal", "").strip()
    study_time = data.get("study_time", "60").strip()

    common = f"""
You are an expert college learning assistant inside an LMS.

Student name: {student}
Course/subject: {course}
Topic: {topic}
Academic level: {level}
Study time available: {study_time} minutes
Learning goal: {goal or "Understand the topic and prepare for assessment."}

Rules:
1. Use accurate, student-friendly explanations.
2. Do not invent citations, facts, or references.
3. Match the difficulty to the student's level.
4. Prefer headings, numbered steps, bullets, tables, and examples.
5. If a question is ambiguous, state a reasonable assumption.
6. End with 3 short "Key Takeaways".
"""

    if mode == "study_plan":
        task = """
Create a personalized study plan for this topic.
Include:
- Learning objectives
- Prerequisites
- A time-boxed sequence of study activities
- What to read/learn in each stage
- Practice tasks
- A mini self-assessment
- Exam tips
"""
    elif mode == "explain":
        task = """
Explain the topic from basics to intermediate level.
Include:
- Simple definition
- Why it matters
- Core concepts
- Step-by-step explanation
- One practical/technical example
- Common mistakes
- 5 quick revision questions
"""
    elif mode == "quiz":
        task = """
Create a 10-question quiz for this topic.
Mix conceptual and application questions.
For each question give 4 options (A-D), identify the correct answer,
and provide a one-sentence explanation. Keep the answer key easy to find.
"""
    elif mode == "flashcards":
        task = """
Create 12 concise flashcards.
Format each as:
Card 1
Q: ...
A: ...
Cover definitions, concepts, formulas/steps where relevant, examples, and common mistakes.
"""
    else:
        task = """
Act as a general academic tutor. Give a useful, structured learning response
for the student's topic and goal.
"""

    return common + "\nTASK:\n" + task
