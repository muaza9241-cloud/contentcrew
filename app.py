import streamlit as st
import requests

st.set_page_config(page_title="ContentCrew Dashboard", page_icon="🚀", layout="wide")

st.title("🚀 ContentCrew: Agentic AI Platform")
st.markdown("Full-stack workspace for content production powered by FastAPI & Streamlit.")

# Backend Health Check Section
st.subheader("Backend Status")
try:
    response = requests.get("http://127.0.0.1:8000/health", timeout=3)
    if response.status_code == 200:
        st.success("API healthy at http://127.0.0.1:8000")
        st.json(response.json())
    else:
        st.warning("Backend is responding, but with issues.")
except:
    st.error("Backend is not reachable. Start it with `python -m uvicorn backend.main:app --reload --port 8000`.")

st.divider()

# Content Generation Section
st.subheader("✨ AI Content Generation Studio")

with st.form("generation_form"):
    user_prompt = st.text_area("Enter your content brief or prompt:", placeholder="e.g., Write a detailed article on AI automation...")
    submit_button = st.form_submit_button("Generate Content", type="primary")

if submit_button:
    if user_prompt.strip():
        with st.spinner("ContentCrew AI agents are crafting your content..."):
            try:
                res = requests.post("http://127.0.0.1:8000/api/generate", json={"prompt": user_prompt})
                if res.status_code == 200:
                    data = res.json()
                    st.success("Content Generated Successfully!")
                    st.markdown(data.get("content"))
                else:
                    st.error("Failed to generate content from backend API.")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a valid prompt first!")

# Context Images Section
st.sidebar.title("📁 Context Workspace")
st.sidebar.markdown("Drop reference images into `context-images/` folder.")
try:
    img_res = requests.get("http://127.0.0.1:8000/context-images", timeout=2)
    if img_res.status_code == 200:
        images = img_res.json().get("images", [])
        if images:
            st.sidebar.success(f"Found {len(images)} reference image(s):")
            for img in images:
                st.sidebar.text(f"• {img}")
        else:
            st.sidebar.info("No reference images found.")
except:
    st.sidebar.warning("Could not fetch context images.")
