# Project Proposal — MechaMentor

## Summary

MechaMentor is an AI-powered troubleshooting assistant for mechatronics students, junior engineers, and makers. It collects structured fault information and returns a safe, ranked diagnostic plan rather than an unfocused chatbot response.

## Target users

- Mechatronics and engineering students
- Junior maintenance or automation engineers
- Makers working on low-risk educational systems

## Problem

Beginners often troubleshoot by guessing. This wastes time, may introduce new faults, and may create safety risks.

## Solution flow

1. Collect system category, symptom, observations, recent changes, constraints, and experience level.
2. Validate the input.
3. Build a named system prompt and a structured user prompt.
4. Call the Groq Chat Completions API.
5. Display a ranked Markdown plan.
6. Store the result in session history and allow JSON export.

## Why AI is suitable

Troubleshooting requires interpreting incomplete natural-language evidence, organising hypotheses, and adapting explanations to the user's experience. The system prompt controls scope, safety, uncertainty, and output structure.

## Core scope

- Groq API integration
- Streamlit interface
- Structured troubleshooting output
- Error handling
- Session history and JSON export
