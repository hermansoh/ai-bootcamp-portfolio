import os
import sys
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

if not GEMINI_API_KEY:
    print("Security Error: GEMINI_API_KEY is missing from your .env file!")
    print("Please generate a key at https://aistudio.google.com/ and add it to .env")
    sys.exit(1)