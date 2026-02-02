import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

try:
    from api_client import AgentClient
except ImportError:
    from frontend.api_client import AgentClient

from backend.core.logger import get_logger

logger = get_logger("streamlit_ui")

st.set_page_config(page_title="Clinical Insight Agent", page_icon="🧬", layout="wide")
client = AgentClient()

with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/medical-doctor.png", width=150)
    st.title("🔧 Control Panel")
    st.markdown("---")
    st.markdown("### 📊 System Status")

    if st.button("Check System Health"):
        logger.info("Health check button clicked.")
        with st.spinner("Checking backend connection..."):
            if client.is_alive():
                st.success("Backend is ONLINE ✅")
            else:
                st.error("Backend is OFFLINE ❌")

    st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        logger.info("Chat history cleared by user.")
        st.rerun()

    st.markdown("---")
    st.info("Agent v1.0 - LangGraph & Gemini 2.0")

st.title("🧬 Autonomous Clinical Trial Insight Agent")
st.markdown("Ask questions about clinical trials, protocols, and statistical data.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(
    "Enter your question here (e.g., 'List Phase 3 Diabetes trials')..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Agent is reasoning...*")

        try:
            answer = client.get_answer(prompt)
            message_placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            logger.error(f"UI Error: {e}")
            message_placeholder.error("An unexpected error occurred. Check logs.")
