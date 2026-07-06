from litellm import completion

response = completion(
    model="ollama/gemma4:e2b",
    messages=[{"role": "user", "content": "Hello! Tell me a fun fact."}],
    api_base="http://localhost:11434"
)

print(response["choices"][0]["message"]["content"])