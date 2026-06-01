import streamlit as st
import requests

st.set_page_config(
    page_title="BeagStore AI SRE Assistant",
    page_icon="🤖"
)

st.title("🤖 BeagStore AI SRE Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask Kubernetes, Prometheus or SRE questions...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    try:

        response = requests.post(
            "http://localhost:8000/query",
             json={"text": prompt},
             timeout=120
        )

        data = response.json()

        answer = data.get("answer", "No answer returned")
        results = data.get("results", [])

    except Exception as e:
        answer = f"Error: {e}"
        context = ""

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)

        if results:
            with st.expander("Retrieved Documents"):
                for item in results:
                    st.write(f"- {item}")
