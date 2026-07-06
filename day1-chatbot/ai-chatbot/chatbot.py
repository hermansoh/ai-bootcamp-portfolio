"""
chatbot.py

A terminal chatbot with memory:
  - LiteLLM -> Ollama (llama3.2:3b) for generating replies
  - Mem0 + ChromaDB + Ollama (nomic-embed-text) for remembering facts about the user
"""

import litellm
from mem0 import Memory

# --- Config ---------------------------------------------------------------
OLLAMA_BASE_URL = "http://localhost:11434"

# LiteLLM needs the "ollama/" prefix to route the call to the right provider.
# Switched from gemma4:e2b to llama3.2:3b for much faster responses.
LITELLM_MODEL = "ollama/llama3.2:3b"

# Mem0's internal config just wants the bare model name, not the LiteLLM-style prefix.
MEM0_MODEL = "llama3.2:3b"

USER_ID = "user1"

mem0_config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memories",
            "path": "./chroma_db",
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": OLLAMA_BASE_URL,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": MEM0_MODEL,
            "ollama_base_url": OLLAMA_BASE_URL,
        },
    },
}

memory = Memory.from_config(mem0_config)


# --- Core chat logic --------------------------------------------------------
def get_response(user_input: str) -> str:
    # 1. Search memory for anything relevant to this message.
    relevant = memory.search(user_input, filters={"user_id": USER_ID})

    # Only keep the top 3 most relevant facts, to keep the prompt short and fast.
    memory_texts = [item["memory"] for item in relevant["results"][:3]]

    # 2. Build a prompt that includes those facts as context, if any exist.
    context_block = ""
    if memory_texts:
        context_block = "Known facts about the user:\n" + "\n".join(
            f"- {fact}" for fact in memory_texts
        )

    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant. {context_block}",
        },
        {"role": "user", "content": user_input},
    ]

    # 3. Call the local model through LiteLLM.
    # max_tokens caps how long the reply can be, which keeps generation time down.
    response = litellm.completion(
        model=LITELLM_MODEL,
        messages=messages,
        api_base=OLLAMA_BASE_URL,
        max_tokens=100,
    )
    reply = response["choices"][0]["message"]["content"]

    # 4. Store this turn so mem0 can extract any new facts from it.
    memory.add(f"User: {user_input}\nAssistant: {reply}", user_id=USER_ID)

    return reply


# --- Terminal loop -----------------------------------------------------------
if __name__ == "__main__":
    print("Chatbot ready. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "quit":
            break
        reply = get_response(user_input)
        print(f"Bot: {reply}")