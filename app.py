import streamlit as st
from openai import OpenAI

# --- Page Config ---
st.set_page_config(page_title="Koushik's AI Summarizer", page_icon="📝", layout="centered")

# --- API Client ---
# Ensure GROQ_API_KEY is saved in your Streamlit Cloud Settings > Secrets
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["GROQ_API_KEY"]
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0px;}
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 2rem;}
    .summary-box { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;}
</style>
""", unsafe_allow_html=True)

# --- UI Layout ---
st.markdown('<div class="main-header">AI Smart Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Paste any long article, report, or email and get an instant summary.</div>', unsafe_allow_html=True)

source_text = st.text_area("Paste your text here:", height=250, placeholder="Once upon a time...")

if st.button("Generate Summary ✨", type="primary"):
    if not source_text.strip():
        st.warning("Please paste some text first!")
    else:
        with st.spinner("Analyzing text..."):
            try:
                # Updated model ID to a currently supported version
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert editor. Summarize the provided text into 3-5 clear, concise bullet points. Do not include any introductory fluff."},
                        {"role": "user", "content": source_text}
                    ],
                    temperature=0.5
                )
                
                summary = response.choices[0].message.content
                
                st.success("Summary Generated!")
                st.markdown('<div class="summary-box">', unsafe_allow_html=True)
                st.markdown(summary)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")