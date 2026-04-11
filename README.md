# Voice-Controlled Local AI Agent

A Voice-Controlled AI Agent that accepts audio input via microphone or file upload, accurately classifies the user's intent, and executes corresponding actions locally (file creation, code generation, summarization) via a clean UI.

## Features

* **Audio Input:** Record directly via microphone or upload an audio file securely in the UI.
* **Intelligent Intent Parsing:** Processes the transcript and classifies intent using structured JSON output.
* **Core Actions:** 
  * `create_file`: Safely creates empty files.
  * `write_code`: Automatically generates and saves code.
  * `summarize_text`: Outputs summarized content.
  * `general_chat`: Responds contextually to standard queries.
* **Safe Sandbox Environment:** All file and code generation strictly targets the `/output` directory to prevent accidental system changes.

## System Architecture & Hardware Workarounds

This project handles varying levels of local machine capabilities. Specifically designed and fallback-tested for environments with limited resources **(e.g., AMD Radeon RX 6500M with 8GB RAM)**:

1. **Speech-to-Text (STT):**
   * **Local Fallback:** Uses `openai-whisper` (`tiny` model) running purely on CPU.
   * **Fast Performance Mode:** Because 8GB of system RAM restricts local heavy inference, the UI provides a toggle to use **Groq API's Whisper-large-v3** for massive speed improvements.
2. **Intent Classification & LLM Engine:**
   * Running a reliable 8B parameter model (e.g., Llama 3) locally consumes roughly 4.5-5GB RAM, leaving the system severely bottlenecked.
   * Therefore, the **Groq API (Llama 3 8B or 70B)** is utilized for near-instant inference, providing structural intent parsing (`JSON` formatted outputs) and conversational responses.
3. **Frontend:** **Streamlit** is used for the web interface, as it natively introduced a great `st.audio_input` widget replacing the need for external tools.

## Setup Instructions

### Prerequisites
* Python 3.10+
* Free Groq API Key (from [console.groq.com](https://console.groq.com))
* [FFmpeg](https://ffmpeg.org/download.html) installed on your system (Required for Whisper local audio processing).

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-link>
   cd local_ai_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   Rename `.env.example` to `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
   *(Alternatively, you can just paste it directly into the settings field on the Streamlit Web UI).*

### Running the App

Start the Streamlit server:
```bash
streamlit run app.py
```
This will launch the Web UI locally.

## Example Usage flow

1. Open the UI.
2. Click the microphone and say: *"Create a python file called hello.py."*
3. Click "Process Command".
4. The system transcribes the audio, detects the `create_file` intent, outputs a JSON payload, creates `hello.py` in the `/output` folder, and displays the success message.
