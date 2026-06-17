import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WHISPER_MODEL = "whisper-large-v3"
API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

def transcribe_audio(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {
            "text": "",
            "error": f"Audio file not found at: {file_path}",
            "mode": "groq_whisper_error"
        }

    if not GROQ_API_KEY:
        return {
            "text": "",
            "error": "GROQ_API_KEY is missing. Please add it to your .env file.",
            "mode": "groq_whisper_error"
        }

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
            
        }

        with open(file_path, "rb") as f:
            files = {
                "file": (os.path.basename(file_path), f)
            }
            data = {
                "model": WHISPER_MODEL,
                "language": "bg",  
                "response_format": "json"
            }


            response = requests.post(API_URL, headers=headers, files=files, data=data)

        if response.status_code != 200:
            return {
                "text": "",
                "error": f"Groq API Error {response.status_code}: {response.text}",
                "mode": "groq_whisper_http_error"
            }

        
        response_json = response.json()
        transcribed_text = response_json.get("text", "").strip()

        return {
            "text": transcribed_text,
            "mode": "groq_whisper_serverless",
            "model_used": WHISPER_MODEL
        }

    except Exception as e:
        return {
            "text": "",
            "error": f"Groq Whisper transcription failed: {str(e)}",
            "mode": "groq_whisper_exception"
        }