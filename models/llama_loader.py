# Earlier I tried to use BgGPT-Gemma-2-2.6B-IT-v1.0 for better answers but it was not available at that time.
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

def ask_bggpt_online(prompt: str, max_new_tokens: int = 512) -> str:
    if not prompt.strip():
        return ""

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=max_new_tokens,
            temperature=0.1,  
            seed=42
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Cloud Model Connection Error: {str(e)}"