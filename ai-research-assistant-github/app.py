"""Streamlit interface for the AI Research Assistant."""

from uuid import uuid4

import streamlit as st

from agent import ask_llm

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🔎 AI Research Assistant")
st.markdown(
    "Turn a research question into a structured report with web-backed findings, "
    "visible tool activity, and exportable Markdown."
)

with st.sidebar:
    st.subheader("About this project")
    st.write(
        "An AI research workflow built with Python, the OpenAI Responses API, "
        "Tavily search, and Streamlit."
    )
    st.divider()
    st.caption("**LLM:** gpt-4.1-mini")
    st.caption("**Search tool:** Tavily (`web_search`)")
    st.caption("**Output:** Markdown research report")
    st.divider()
    st.subheader("Try a sample question")
    sample_questions = [
        "Research the benefits and risks of AI agents for small businesses.",
        "Compare popular Python web frameworks for building APIs.",
        "Research practical uses of generative AI in education.",
    ]
    for index, sample in enumerate(sample_questions):
        if st.button(sample, key=f"sample_{index}", use_container_width=True):
            st.session_state.pending_question = sample
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.chat = []
        st.session_state.agent_history = []
        st.session_state.pending_question = ""
        st.rerun()

if "chat" not in st.session_state:
    st.session_state.chat = []
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

if not st.session_state.chat:
    st.info(
        "Ask a question below to begin. For current or research-heavy topics, "
        "the agent may call the web search tool before preparing a report."
    )

for entry in st.session_state.chat:
    with st.chat_message(entry["role"]):
        if entry["role"] == "assistant":
            st.markdown(entry["content"])
            if entry.get("report"):
                with st.expander("Copy or download report"):
                    st.code(entry["content"], language="markdown")
                    st.download_button(
                        "Download Markdown report",
                        data=entry["content"],
                        file_name="research-report.md",
                        mime="text/markdown",
                        key=f"download_{entry['id']}",
                    )
        else:
            st.markdown(entry["content"])

question = st.chat_input(
    "Ask a research question…",
)

if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = ""

if question:
    st.session_state.chat.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        progress = st.status("Preparing your research…", expanded=True)
        report_placeholder = st.empty()
        streamed_report = [""]

        def on_status(message: str) -> None:
            progress.write(message)
            progress.update(label=message, state="running")

        def on_report_delta(delta: str) -> None:
            streamed_report[0] += delta
            report_placeholder.markdown(streamed_report[0] + " ▌")

        answer = ask_llm(
            question,
            history=st.session_state.agent_history,
            on_status=on_status,
            on_report_delta=on_report_delta,
        )

        report_placeholder.markdown(answer)
        progress.update(label="Finished", state="complete", expanded=False)

        report_id = uuid4().hex
        st.session_state.chat.append(
            {
                "role": "assistant",
                "content": answer,
                "report": True,
                "id": report_id,
            }
        )

        with st.expander("Copy or download report", expanded=True):
            st.code(answer, language="markdown")
            st.download_button(
                "Download Markdown report",
                data=answer,
                file_name="research-report.md",
                mime="text/markdown",
                key=f"download_current_{report_id}",
            )
