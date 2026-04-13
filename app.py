import streamlit as st
import os
import json
import tempfile
import PyPDF2
from dotenv import load_dotenv
from groq import Groq

from audio_processor import transcribe_audio_local, transcribe_audio_groq
from agent_core import parse_intent
from tools import execute_intent, ensure_output_dir

# Load environment variables
load_dotenv()

# Ensure output dir exists on startup
ensure_output_dir()

# Initialize memory in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0
if "pending_alert" not in st.session_state:
    st.session_state.pending_alert = None
if "pending_filename" not in st.session_state:
    st.session_state.pending_filename = None
if "pending_intent" not in st.session_state:
    st.session_state.pending_intent = None
if "draft_transcription" not in st.session_state:
    st.session_state.draft_transcription = None

st.set_page_config(page_title="Voice-Controlled AI Agent", page_icon="🎙️", layout="wide")

st.title("🎙️ Voice-Controlled Local AI Agent")

st.markdown("""
**Hardware Note for Reviewer:** 
This system implements a smart fallback utilizing the **Groq API** for STT (`whisper-large-v3`) and LLM processing (`llama3-8b`). 
This handles the specific machine constraints (8GB RAM, AMD GPU) which makes running local LLMs and large Whisper models very slow or unstable. 
However, a local Whisper (`tiny`, CPU) option is included as required by the assignment constraints. 
*All file creation operations are safely restricted to the `output/` folder.*
""")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    api_key_input = st.text_input(
        "Groq API Key (If not in .env)",
        type="password",
        placeholder="gsk_..."
    )
    
    stt_engine_choice = st.radio(
        "Speech-To-Text Engine",
        options=["Groq API (Fast)", "Local Whisper CPU (Slow)"],
        index=0
    )

# Use api key from input or from env
api_key = api_key_input or os.environ.get("GROQ_API_KEY", "")

# We need to explicitly check if st.audio_input is available in this Streamlit version (>=1.39)
# Streamlit provides a built-in microphone/upload component now
# Add option to upload file or use microphone
st.markdown("### 1. Provide Audio Command")

tab1, tab2 = st.tabs(["🎙️ Microphone (Live Wave)", "📁 Upload File"])

with tab1:
    # Streamlit's native audio input provides the visual audio wave they want
    mic_audio = st.audio_input("Record a voice command", key=f"mic_{st.session_state.audio_key}")
    if mic_audio:
        final_audio_bytes = mic_audio.read()
        file_suffix = ".wav"
    else:
        final_audio_bytes = None
        file_suffix = ""

with tab2:
    uploaded_file = st.file_uploader("Upload an audio file or PDF document", type=["wav", "mp3", "m4a", "ogg", "flac", "pdf"])
    if uploaded_file is not None:
        file_suffix = "." + uploaded_file.name.split('.')[-1]
        if file_suffix.lower() == ".pdf":
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    if page.extract_text():
                        pdf_text += page.extract_text() + "\n"
                st.session_state.pdf_text_extracted = pdf_text
                st.success(f"📄 PDF '{uploaded_file.name}' loaded successfully! Click Process Command to summarize it.")
                final_audio_bytes = b"dummy"
            except Exception as e:
                st.error(f"Failed to read PDF: {e}")
                final_audio_bytes = None
        else:
            final_audio_bytes = uploaded_file.read()
            st.audio(final_audio_bytes, format=f"audio/{uploaded_file.name.split('.')[-1]}")

        
if final_audio_bytes is not None and not st.session_state.get("draft_transcription"):
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("📝 Transcribe / Extract", type="primary"):
            transcribe_clicked = True
        else:
            transcribe_clicked = False
            
    with col_btn2:
        if st.button("🗑️ Discard & Re-Record"):
            st.session_state.audio_key += 1
            st.rerun()
            
    if transcribe_clicked:
        with st.spinner("Extracting text..."):
            if not api_key:
                st.error("Error: Groq API Key is missing. Please enter it in the settings or .env file.")
                st.stop()
            try:
                client = Groq(api_key=api_key)
            except Exception as e:
                st.error(f"Error initializing Groq client: {str(e)}")
                st.stop()
            
            if file_suffix.lower() == ".pdf":
                transcription = f"Please provide a concise summary of the following document:\n\n{st.session_state.pdf_text_extracted[:20000]}"
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                    tmp_file.write(final_audio_bytes)
                    audio_filepath = tmp_file.name
                if stt_engine_choice == "Groq API (Fast)":
                    transcription = transcribe_audio_groq(client, audio_filepath)
                else:
                    transcription = transcribe_audio_local(audio_filepath)
                if os.path.exists(audio_filepath):
                    os.remove(audio_filepath)
            
            st.session_state.draft_transcription = transcription
            st.rerun()

if st.session_state.get("draft_transcription"):
    st.markdown("### 2. Review and Edit Command")
    edited_text = st.text_area("Edit text before agent processes it:", value=st.session_state.draft_transcription, height=150)
    
    col_proc1, col_proc2 = st.columns([1, 4])
    with col_proc1:
        if st.button("🚀 Confirm & Execute", type="primary"):
            process_clicked = True
        else:
            process_clicked = False
    with col_proc2:
        if st.button("❌ Cancel Edit"):
            st.session_state.draft_transcription = None
            st.rerun()
            
    if process_clicked:
        transcription = edited_text
        with st.spinner("Processing Intent..."):
            if not api_key:
                st.error("Missing Groq API Key")
                st.stop()
            client = Groq(api_key=api_key)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📝 Final Input")
                if file_suffix.lower() == ".pdf":
                    st.info(f"[PDF Input Verified - Proceeding to Summation]")
                else:
                    st.info(transcription)

            if transcription.startswith("Error"):
                st.error("Failed to transcribe audio.")
            else:
                # 2. Intent Parsing
                with col2:
                    st.subheader("🧠 Detected Intent")
                    intent_data = parse_intent(client, transcription, st.session_state.chat_history)
                    st.json(intent_data)

                # 3. Tool Execution & Human-in-the-Loop Interception
                target_intent = intent_data.get("intent")
                if target_intent in ["delete_file", "create_file", "write_code"]:
                    st.session_state.pending_alert = target_intent
                    st.session_state.pending_filename = intent_data.get("filename", "unknown_file.txt")
                    st.session_state.pending_intent = intent_data
                    st.session_state.pending_transcription = transcription
                    
                    target_msg = intent_data.get("message", f"I am about to {target_intent} for `{st.session_state.pending_filename}`.")
                    st.warning(f"🤖 **Agent:** '{target_msg}'\n\n⚠️ **Paused Execution:** Please confirm below if you want to proceed.")
                else:
                    st.subheader("⚡ Execution & Result")
                    result_data = execute_intent(client, intent_data, transcription)
                    
                    st.success(f"**Action Taken:** {result_data.get('action', 'Unknown')}")
                    st.code(result_data.get('result', 'No result provided.'), language="plaintext")
                    
                    # Append to session history (Memory)
                    memory_result = result_data.get("result", "")
                    if "code" in intent_data:
                        memory_result += f"\n\nCode I wrote:\n{intent_data['code']}"
                    
                    st.session_state.chat_history.append({
                        "user": transcription,
                        "intent": intent_data.get("intent", "unknown"),
                        "action": result_data.get("action", "unknown"),
                        "result": memory_result
                    })

            # Reset draft after processing
            st.session_state.draft_transcription = None
            
# --- Human-in-the-loop Alert ---
if st.session_state.get("pending_alert"):
    action_type = st.session_state.pending_alert
    filename = st.session_state.pending_filename
    
    if action_type == "delete_file":
        st.error(f"🚨 **Confirm Deletion:** Are you sure you want to permanently delete `output/{filename}`?")
    else:
        st.info(f"🛡️ **Confirm Operation:** I am going to write/modify `output/{filename}`. Do you allow this?")
        
    alert_col1, alert_col2 = st.columns(2)
    with alert_col1:
        if st.button("✅ Yes, Proceed", type="primary"):
            # Initialize groq client for execution just in case
            proceed_client = Groq(api_key=api_key)
            result_data = execute_intent(proceed_client, st.session_state.pending_intent, st.session_state.pending_transcription)
            
            memory_result = result_data.get("result", "")
            if "code" in st.session_state.pending_intent:
                memory_result += f"\n\nCode I wrote:\n{st.session_state.pending_intent['code']}"
                
            st.session_state.chat_history.append({
                "user": st.session_state.pending_transcription,
                "intent": action_type,
                "action": result_data.get("action", "unknown"),
                "result": memory_result
            })
            st.session_state.pending_alert = None
            st.session_state.pending_filename = None
            st.session_state.pending_intent = None
            st.session_state.pending_transcription = None
            st.rerun()
            
    with alert_col2:
        if st.button("❌ Cancel"):
            st.session_state.chat_history.append({
                "user": st.session_state.pending_transcription,
                "intent": action_type,
                "action": "Cancelled",
                "result": f"User cancelled the operation on `{filename}`."
            })
            st.session_state.pending_alert = None
            st.session_state.pending_filename = None
            st.session_state.pending_intent = None
            st.session_state.pending_transcription = None
            st.rerun()
            
# 4. Display Chat History (Bonus Requirement)
if len(st.session_state.chat_history) > 0:
    st.divider()
    st.markdown("### 🗂️ Session History (Memory)")
    for i, msg in enumerate(reversed(st.session_state.chat_history)):
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(f"**Action:** {msg['action']}\n\n**Result:**\n```\n{msg['result'][:500]}{'...' if len(msg['result']) > 500 else ''}\n```")
