import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Put it in backend/.env")

client = genai.Client(api_key=API_KEY)

def generate_learning_content(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=3000,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("The GenAI model returned an empty response.")
    return text
