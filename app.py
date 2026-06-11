import streamlit as st
from utils.chatbot import get_response, SYSTEM_PROMPT
from utils.pdf_reader import extract_text
from utils.safety import check_emergency
from database.db import init_db, save_message

# Initialize DB
init_db()

# Page config
st.set_page_config(
    page_title="AI Medical Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Header (Light Blue Theme)
st.markdown(
    """
    <h1 style='text-align: center; color:#0369a1;'>🏥 AI Medical Assistant</h1>
    <p style='text-align: center; color:#0284c7; font-size:16px;'>
    Smart healthcare chatbot for basic medical guidance
    </p>
    """,
    unsafe_allow_html=True
)

# Disclaimer (Light Blue Style)
st.markdown(
    """
    <div style="background-color:#e0f2fe;padding:12px;border-radius:10px;
                color:#075985;border:1px solid #bae6fd; margin-bottom:15px;">
    ⚠️ This chatbot provides general advice only. Consult a doctor for serious issues.
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.markdown("## 📄 Upload Medical Report")
pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.write("AI Medical Assistant using LLM for healthcare queries.")

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.rerun()

pdf_text = ""
if pdf_file:
    pdf_text = extract_text(pdf_file)
    st.sidebar.success("✅ PDF uploaded successfully!")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat
for msg in st.session_state.messages[1:]:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("💬 Enter your symptoms or question...")

if user_input:

    # Emergency detection
    if check_emergency(user_input):
        st.error("🚨 This may be serious. Seek immediate medical attention!")

    # Add PDF context
    if pdf_text:
        user_input = f"Based on this medical report:\n{pdf_text}\n\nQuestion: {user_input}"

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_message("user", user_input)

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # AI response
    with st.spinner("🤖 Thinking..."):
        reply = get_response(st.session_state.messages)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    save_message("assistant", reply)

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)