import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("🤖 RAG Customer Support Assistant")

# -----------------------------
# Sidebar (Upload Section)
# -----------------------------
st.sidebar.header("📄 Upload Document")

uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{API_URL}/upload", files=files)

        if res.status_code == 200:
            st.sidebar.success("✅ PDF processed successfully")
        else:
            st.sidebar.error("❌ Upload failed")

# -----------------------------
# Main Query Section
# -----------------------------
st.subheader("Ask a Question")

query = st.text_input("Enter your question here...")

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{API_URL}/query",
                json={"query": query}
            )

            if res.status_code == 200:
                data = res.json()

                # -----------------------------
                # Answer
                # -----------------------------
                st.subheader("🧠 Answer")
                st.write(data["answer"])

                # -----------------------------
                # Metadata
                # -----------------------------
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Intent**")
                    st.write(data["intent"])

                with col2:
                    st.markdown("**Escalated**")
                    st.write(data["escalated"])

                # -----------------------------
                # Sources
                # -----------------------------
                st.subheader("📚 Retrieved Context")

                for i, chunk in enumerate(data["chunks_used"]):
                    with st.expander(f"Chunk {i+1}"):
                        st.write(chunk)

            else:
                st.error("❌ Failed to get response")