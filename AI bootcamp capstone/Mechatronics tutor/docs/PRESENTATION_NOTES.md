# Presentation Notes

## Slide 1 — Title

**MechaMentor** — AI Engineering Troubleshooting Assistant  
Herman Soh

A focused AI application that converts engineering fault descriptions into safe, ranked diagnostic plans.

## Slide 2 — The Problem

- Beginners often troubleshoot by guessing.
- Evidence is missed or recorded inconsistently.
- Unsafe or invasive tests may be attempted too early.
- Target users are engineering students and junior engineers.

## Slide 3 — How It Works

```text
User fault description
        ↓
Python validation
        ↓
Named system prompt + structured user prompt
        ↓
Groq API
        ↓
Ranked troubleshooting plan
        ↓
Streamlit display + session export
```

Explain these decisions:

1. Exact headings make output consistent.
2. Safety comes before diagnosis.
3. Low-risk, high-information checks are prioritised.
4. API code is isolated in a service class.
5. Deterministic helpers have unit tests.

## Live demo

1. Embedded controller that will not start
2. Motor that stops under load

## Slide 5 — What I Learned

- The hardest part was preventing false certainty while keeping the response useful.
- Structured headings and explicit safety rules improved consistency.
- Future work: document retrieval and image input.
