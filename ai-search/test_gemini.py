import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))
print("API key length:", len(api_key or ""))

if not api_key:
    raise RuntimeError("GEMINI_API_KEY was not found")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Say hello in one sentence."
)

print(response.text)