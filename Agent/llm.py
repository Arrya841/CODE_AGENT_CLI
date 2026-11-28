import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from Agent.model_router import generate_with_fallback

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=10_000,
            retry_options=types.HttpRetryOptions(
                attempts=2, initial_delay=0.5, max_delay=0.5, jitter=0,
            ),
        ),
    )

def ask_llm(prompt, memory, max_turns=10):
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")
    if client is None:
        raise RuntimeError("GEMINI_API_KEY is missing.")
    user_message = types.Content(
        role= "user",
        parts=[types.Part(text=prompt)]
    )
    contents = memory.get_recent_history(max_turns) + [user_message]
    response = generate_with_fallback(client, contents)
    memory.add_user_message(prompt)
    memory.add_model_message(response)

    return response