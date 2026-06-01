import streamlit as st
from pypdf import PdfReader
import requests

st.title("📄 PDF Knowledge Upload")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success(f"Extracted {len(text)} characters")

    st.text_area(
        "Preview",
        text[:2000],
        height=300
    )

    if st.button("Ingest Into RAG"):

        chunks = [
            text[i:i+1000]
            for i in range(0, len(text), 1000)
        ]

        progress = st.progress(0)

        success_count = 0

        for idx, chunk in enumerate(chunks):

            try:
                response = requests.post(
                    "http://localhost:8000/ingest",
                    json={"text": chunk},
                    timeout=60
                )

                if response.status_code == 200:
                    success_count += 1

            except Exception as e:
                st.error(f"Chunk failed: {e}")

            progress.progress((idx + 1) / len(chunks))

        st.success(
            f"Ingested {success_count}/{len(chunks)} chunks"
        )
