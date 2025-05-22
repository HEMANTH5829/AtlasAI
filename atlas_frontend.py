import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "https://atlas-ai-api.onrender.com/ask "
DEFAULT_API_KEY = "jhfhfahfkjfalfhafh9qhqhg"

# --- STREAMLIT UI ---
st.set_page_config(page_title="🧠 ATLAS AI", layout="centered")
st.title("🧠 ATLAS AI – Ask an Expert-Level Question")

st.markdown("""
Ask any question, and ATLAS will:
- Use multiple reasoning paths
- Cross-validate answers
- Provide expert-level responses
- Show sources and reasoning steps
""")

user_question = st.text_input("Enter your question:", placeholder="E.g., What are the causes of World War II?")

if st.button("Get Answer"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking through multiple paths..."):
            headers = {"x-api-key": DEFAULT_API_KEY}
            payload = {"question": user_question}

            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                data = response.json()

                if not data.get("success", True):
                    st.error("Error from API: " + data.get("consensus_answer", "Unknown error"))
                else:
                    st.subheader("🔍 Reasoning Paths")
                    for path, answer in data["reasoning_paths"].items():
                        st.markdown(f"**{path}:** {answer}")

                    st.subheader("✅ Final Consensus Answer")
                    st.markdown(data["consensus_answer"])

                    st.subheader("📚 Context Sources")
                    for idx, source in enumerate(data["context_used"], 1):
                        st.markdown(f"**Source {idx}:** {source[:300]}...")

            except Exception as e:
                st.error(f"Failed to reach API: {str(e)}")
