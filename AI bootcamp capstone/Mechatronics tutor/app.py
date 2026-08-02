"""!
@file app.py
@brief Streamlit interface for the MechaMentor capstone project.

MechaMentor is an AI engineering troubleshooting assistant. It accepts a
structured fault description, builds a deliberately constrained system prompt,
calls the Groq API, and displays a safe, ranked diagnostic plan.
"""

from __future__ import annotations
import streamlit as st
from src.config import AppConfig, ConfigurationError
from src.groq_service import GroqTroubleshootingService
from src.history import add_history_record, export_history_json
from src.models import TroubleshootingRequest
from src.prompting import SYSTEM_PROMPT, build_user_prompt
from src.validators import validate_request


## @brief Configure the Streamlit page.
def configure_page() -> None:
    st.set_page_config(page_title="MechaMentor", page_icon="🛠️", layout="wide")


## @brief Initialise Streamlit session-state values.
def initialise_session_state() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []


## @brief Render the project title, purpose, and safety notice.
def render_header() -> None:
    st.title("🛠️ MechaMentor")
    st.subheader("AI Engineering Troubleshooting Assistant")
    st.write(
        "Describe an engineering fault and receive a safe, ranked diagnostic "
        "plan with likely causes, checks, expected observations, and an escalation point."
    )
    st.warning(
        "Educational guidance only. Follow equipment manuals and safety procedures. "
        "Stop before tests involving hazardous voltage, stored energy, pressure, heat, "
        "or uncontrolled movement."
    )


## @brief Render the troubleshooting form.
## @return A tuple containing the submitted flag and request.
def render_request_form() -> tuple[bool, TroubleshootingRequest]:
    with st.form("troubleshooting_form"):
        left, right = st.columns(2)
        with left:
            system_type = st.selectbox(
                "System category",
                [
                    "Embedded system / microcontroller",
                    "Motor and drive system",
                    "Sensor and instrumentation",
                    "Power supply / electrical",
                    "Mechanical assembly",
                    "Robot / automation system",
                    "Software / communication",
                    "Other",
                ],
            )
            experience_level = st.selectbox(
                "Your experience level", ["Beginner", "Intermediate", "Advanced"]
            )
            symptom = st.text_area(
                "Main symptom",
                placeholder="Example: The motor starts but stops under load.",
                height=130,
            )
        with right:
            observations = st.text_area(
                "Observed evidence",
                placeholder="Example: Driver fault LED turns on and supply voltage drops.",
                height=130,
            )
            recent_changes = st.text_area(
                "Recent changes",
                placeholder="Example: Increased load, changed firmware, or rewired sensor.",
                height=100,
            )
            constraints = st.text_area(
                "Constraints or safety concerns",
                placeholder="Example: Maximum safe test current is 2 A.",
                height=100,
            )
        submitted = st.form_submit_button(
            "Generate troubleshooting plan", type="primary", use_container_width=True
        )
    return submitted, TroubleshootingRequest(
        system_type=system_type,
        symptom=symptom,
        observations=observations,
        recent_changes=recent_changes,
        constraints=constraints,
        experience_level=experience_level,
    )


## @brief Generate and display a troubleshooting response.
## @param request Structured troubleshooting input from the user.
def process_request(request: TroubleshootingRequest) -> None:
    errors = validate_request(request)
    if errors:
        for error in errors:
            st.error(error)
        return
    try:
        config = AppConfig.from_environment()
        service = GroqTroubleshootingService(config)
        with st.spinner("Building a diagnostic plan..."):
            response = service.generate_plan(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=build_user_prompt(request),
            )
        st.success("Troubleshooting plan generated.")
        st.markdown(response)
        add_history_record(st.session_state.history, request, response)
    except ConfigurationError as error:
        st.error(str(error))
    except Exception as error:
        st.error(
            "The AI service could not complete the request. Check your internet "
            "connection, API key, and model name."
        )
        st.caption(f"Technical detail: {error}")


## @brief Render previous results and a JSON export button.
def render_history() -> None:
    st.divider()
    st.header("Session history")
    if not st.session_state.history:
        st.info("No troubleshooting plans have been generated in this session.")
        return
    st.download_button(
        "Download session history",
        data=export_history_json(st.session_state.history),
        file_name="mechamentor_session.json",
        mime="application/json",
    )
    for index, record in enumerate(reversed(st.session_state.history), start=1):
        title = f"{index}. {record['request']['system_type']} — {record['created_at']}"
        with st.expander(title):
            st.markdown("**Symptom**")
            st.write(record["request"]["symptom"])
            st.markdown("**AI troubleshooting plan**")
            st.markdown(record["response"])


## @brief Application entry point.
def main() -> None:
    configure_page()
    initialise_session_state()
    render_header()
    submitted, request = render_request_form()
    if submitted:
        process_request(request)
    render_history()


if __name__ == "__main__":
    main()
