from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")

client = genai.Client(api_key=GEMINI_KEY)

def ask_ai_something(contents:str):
    model="gemini-2.5-flash-lite"
    resp = client.models.generate_content(
        model = model,
        contents=contents
    )
    
    return resp.text