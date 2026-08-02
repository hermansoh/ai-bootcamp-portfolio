# MechaMentor — AI Engineering Troubleshooting Assistant

## 1. Project Title and Description

**MechaMentor** is a focused AI troubleshooting assistant for mechatronics students, junior engineers, and makers. It converts a structured problem description into a safe, ranked diagnostic plan, including likely causes, checks, expected observations, and escalation guidance.

## 2. Problem Statement

Engineering faults are often difficult to troubleshoot because symptoms can have many possible causes, and beginners may test components in an unsafe or inefficient order. MechaMentor helps users organise evidence, identify likely causes, and follow a systematic troubleshooting sequence without pretending to replace a qualified engineer or safety procedure.

## 3. Technology Stack

- Python 3.10+
- Streamlit
- Groq Python SDK
- `python-dotenv`
- Groq Chat Completions API
- Model configured through `GROQ_MODEL` in `.env`

## 4. Setup Instructions

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment.

   **Windows Command Prompt**
   ```cmd
   py -3 -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux/WSL**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and add your Groq key.
6. Run tests:
   ```bash
   python -m unittest discover -s tests -v
   ```
7. Start the app:
   ```bash
   streamlit run app.py
   ```

## 5. Usage Examples

### Example 1 — Embedded controller does not start

Input a powered board that will not run firmware and cannot connect to the debugger. The app should return likely causes, safe first checks, expected observations, and an escalation point.

### Example 2 — Motor runs intermittently

Input a motor that starts, stops under load, and triggers a driver fault LED. The app should rank possible causes such as supply sag, overcurrent, overheating, wiring, or mechanical load.

## 6. Known Limitations

1. Output quality depends on the accuracy and completeness of the user’s description.
2. The AI cannot physically inspect equipment or verify measurements.

## 7. Future Improvements

1. Add optional image input for wiring diagrams or error screenshots.
2. Add manual and course-note retrieval for grounded answers.

## Safety Notice

MechaMentor does not replace qualified engineering judgement, lockout/tagout procedures, equipment manuals, or workplace safety rules.
