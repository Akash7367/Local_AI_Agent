import os
import whisper

# Load the model lazily so it doesn't slow down app startup
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print("Loading local Whisper model (tiny) on CPU...")
        # We use the tiny model to ensure it runs comfortably on 8GB RAM CPU
        _whisper_model = whisper.load_model("tiny", device="cpu")
    return _whisper_model

def transcribe_audio_local(audio_filepath: str) -> str:
    """
    Transcribes audio using a local Whisper model.
    Required for systems where strict local processing is needed.
    """
    try:
        model = get_whisper_model()
        result = model.transcribe(audio_filepath)
        return result["text"].strip()
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def transcribe_audio_groq(client, audio_filepath: str) -> str:
    """
    Transcribes using Groq's high-speed Whisper API endpoint.
    Ideal for lower-spec hardware like 8GB RAM + AMD GPU where local inference
    with larger models would be prohibitively slow.
    """
    try:
        with open(audio_filepath, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", file.read()),
                model="whisper-large-v3-turbo",
                prompt="Specify context or spelling if needed",
                response_format="json",
                language="en",
                temperature=0.0
            )
            return transcription.text.strip()
    except Exception as e:
         return f"Error with Groq STT: {str(e)}"
