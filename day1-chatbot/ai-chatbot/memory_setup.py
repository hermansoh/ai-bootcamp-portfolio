"""
memory_setup.py

Local chatbot memory using mem0, Ollama, and ChromaDB.

Prereqs:
  - Ollama running locally (default: http://localhost:11434)
  - Models pulled: nomic-embed-text, llama3.2:3b
  - pip install mem0ai chromadb ollama
"""

from mem0 import Memory

MODEL = "llama3.2:3b"
OLLAMA = "http://localhost:11434"

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "my_memories",
            "path": "./chroma_db",
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": OLLAMA,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": MODEL,
            "ollama_base_url": OLLAMA,
        },
    },
}

memory = Memory.from_config(config)

memory.add("My name is Alex and I study at DigiPen", user_id="student1")

results = memory.search("What is my name?", filters={"user_id": "student1"})
print(results)