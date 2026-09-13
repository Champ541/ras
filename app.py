import os
import streamlit as st
from rag import RASRetriever, generate_answer

st.set_page_config(page_title="RAS AI | IEEE RAS VIT Chennai", page_icon="🤖", layout="centered")

# Streamlit Cloud stores secrets in st.secrets, while local runs can use env vars.
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

st.markdown("""
<style>
.block-container {max-width: 900px; padding-top: 2rem;}
.hero {padding: 1.4rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px; margin-bottom: 1.2rem;}
.badge {font-size:.8rem; letter-spacing:.08em; text-transform:uppercase; opacity:.7;}
.source {padding:.7rem .9rem; border-left:3px solid #ff4b4b; background:rgba(128,128,128,.08); border-radius:0 10px 10px 0; margin:.45rem 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<div class="badge">IEEE Robotics & Automation Society • VIT Chennai</div>
<h1>🤖 RAS AI</h1>
<p>Ask questions about IEEE RAS VIT Chennai and get answers grounded in publicly available chapter information.</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_retriever():
    return RASRetriever("data/knowledge_base.json")

retriever = load_retriever()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About this RAG")
    st.write("Retrieval uses TF-IDF over a curated public-information knowledge base. If a Gemini API key is configured, Gemini turns the retrieved evidence into a natural-language answer.")
    st.caption("The assistant is designed to avoid inventing facts outside its retrieved context.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for s in message["sources"]:
                    st.markdown(f'<div class="source"><b>{s["title"]}</b><br>{s["url"]}</div>', unsafe_allow_html=True)

question = st.chat_input("Ask about IEEE RAS VIT Chennai…")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    docs = retriever.retrieve(question, k=5)
    answer = generate_answer(question, docs)

    sources = []
    seen = set()
    for d in docs:
        if d["url"] not in seen:
            sources.append({"title": d["title"], "url": d["url"]})
            seen.add(d["url"])

    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.expander("Retrieved sources"):
            for s in sources:
                st.markdown(f'<div class="source"><b>{s["title"]}</b><br>{s["url"]}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role":"user", "content":question})
    st.session_state.messages.append({"role":"assistant", "content":answer, "sources":sources})
