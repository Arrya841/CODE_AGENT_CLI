import os
from dotenv import load_dotenv
from google import genai
from Agent.model_router import generate_with_fallback

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing environment")
client = genai.Client(api_key=api_key)

def ask_llm(prompt):
    return generate_with_fallback(client, prompt)