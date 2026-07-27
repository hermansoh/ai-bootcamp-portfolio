import requests
import streamlit as st
from typing import Dict


OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:1.5b"


def ask_ollama(
    prompt: str,
    model: str = MODEL_NAME,
    temperature: float = 0.2
) -> str:
    """Send one prompt to Ollama and return the response."""

    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 500,
        },
    }

    response = requests.post(
        url,
        json=payload,
        timeout=300,
    )

    if not response.ok:
        try:
            error_message = response.json().get("error", response.text)
        except ValueError:
            error_message = response.text

        raise RuntimeError(
            f"Ollama request failed with status "
            f"{response.status_code}: {error_message}"
        )

    return response.json().get("response", "").strip()


def make_code_explainer_prompt(code_snippet: str) -> str:
    return f"""
You are a helpful programming tutor.

Review the following Python code:

```python
{code_snippet}
```

Answer using numbered sections:

1. Explain what the code does.
2. Explain the important lines.
3. Identify any bugs, risks, or confusing parts.
4. Provide a corrected or improved version if needed.

Use simple language suitable for a beginner.
""".strip()


def make_debug_prompt(
    error_message: str,
    code_snippet: str = ""
) -> str:
    if code_snippet.strip():
        code_section = f"""
```python
{code_snippet}
```
"""
    else:
        code_section = "No code snippet was provided."

    return f"""
You are a helpful Python debugging assistant.

Error message:

```text
{error_message}
```

Code:

{code_section}

Answer using numbered sections:

1. Explain the most likely cause.
2. Identify the problem line.
3. Provide a simple fix.
4. Provide a safer rewritten version.
5. Briefly explain the changes.
""".strip()


def make_testcase_prompt(code_snippet: str) -> str:
    return f"""
You are a software testing assistant.

Review the following Python code:

```python
{code_snippet}
```

Suggest suitable test cases.

For each test case, provide:

1. Input
2. Expected output
3. Why the test matters

Include normal cases and these edge cases where applicable:

- Empty input
- None
- Wrong data type
- Boundary values
""".strip()


def make_improvement_prompt(code_snippet: str) -> str:
    return f"""
You are an experienced Python code reviewer.

Review the following Python code:

```python
{code_snippet}
```

Answer using numbered sections:

1. Identify readability issues.
2. Identify missing error handling.
3. Provide performance notes.
4. Provide a cleaner rewritten version.
5. Briefly explain each change.
""".strip()


def classify_task(user_request: str) -> str:
    text = user_request.lower()

    debug_keywords = [
        "error",
        "bug",
        "fix",
        "debug",
        "exception",
        "traceback",
        "fails",
    ]

    test_keywords = [
        "test",
        "case",
        "assert",
        "pytest",
        "unittest",
        "coverage",
    ]

    improve_keywords = [
        "improve",
        "refactor",
        "clean",
        "optimise",
        "optimize",
        "rewrite",
        "review",
    ]

    if any(keyword in text for keyword in debug_keywords):
        return "debug"

    if any(keyword in text for keyword in test_keywords):
        return "test"

    if any(keyword in text for keyword in improve_keywords):
        return "improve"

    return "explain"


def developer_assistant(
    user_request: str,
    code_snippet: str = "",
    error_message: str = ""
) -> Dict[str, str]:
    task = classify_task(user_request)

    if task == "debug":
        prompt = make_debug_prompt(
            error_message,
            code_snippet,
        )

    elif task == "test":
        prompt = make_testcase_prompt(code_snippet)

    elif task == "improve":
        prompt = make_improvement_prompt(code_snippet)

    else:
        prompt = make_code_explainer_prompt(code_snippet)

    answer = ask_ollama(prompt)

    return {
        "task": task,
        "answer": answer,
    }


st.set_page_config(
    page_title="Local AI Developer Assistant",
    page_icon="🖥️",
)

st.title("🖥️ Local AI Developer Assistant")
st.caption(
    f"Running locally with Ollama and {MODEL_NAME} — no cloud API used"
)

code_input = st.text_area(
    "Paste your code here",
    height=220,
    placeholder="def divide(a, b):\n    return a / b",
)

error_input = st.text_input(
    "Error message (optional)",
    placeholder="ZeroDivisionError: division by zero",
)

request_input = st.text_input(
    "What do you want?",
    placeholder="Explain this, debug this, suggest tests, or refactor this",
)

if st.button("Run assistant", type="primary"):
    if not request_input.strip():
        st.warning("Enter a request first.")

    elif not code_input.strip():
        st.warning("Paste some code first.")

    else:
        try:
            with st.spinner("Thinking locally..."):
                result = developer_assistant(
                    request_input,
                    code_input,
                    error_input,
                )

            st.markdown(
                f"**Classified as:** `{result['task']}`"
            )

            st.markdown(result["answer"])

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to Ollama. Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The model took too long to respond. Try again or use a smaller model."
            )

        except Exception as exc:
            st.error(f"Error: {exc}")