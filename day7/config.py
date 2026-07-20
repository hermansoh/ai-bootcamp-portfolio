import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Read the environment variables with safe defaults
MODEL_NAME = os.getenv("MODEL_NAME")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")