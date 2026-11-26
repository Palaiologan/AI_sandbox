import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

# 1. Sidebar
with st.sidebar:
    model = st.selectbox("Model", ["gpt-6-luna", "gpt-6.1-terra"])
    os.environ["MODEL_NAME"] = model

# 2. Import Graph
from graph_logic import flowchart

st.title("📚 Book Summarizer")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Generate"):
        loader = PyPDFLoader("temp.pdf")
        pages = loader.load()
        
        # Run graph
        initial_state = {
            "pages": pages,
            "book_text": "",
            "outline": "",
            "research_notes": "",
            "draft": "",
            "critique": "",
            "revision_count": 0
            }

        status_text = st.empty()
        output_area = st.container()
        config = {"configurable": {"thread_id": "1"}}

        for updates in flowchart.stream(initial_state, config=config):
            for nodename, nodeout in updates.items():
                if nodename == 'prep':
                    continue
                
                # Update status bar instead of printing
                status_text.info(f"⚙️ Running Agent: **{nodename.upper()}**")
                
                # Optionally show intermediate results in an expander
                with output_area.expander(f"📄 {nodename} Output", expanded=False):
                    for k, v in nodeout.items():
                        if v:
                            st.markdown(v)