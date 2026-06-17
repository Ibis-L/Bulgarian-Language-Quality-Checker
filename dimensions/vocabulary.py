import re
import json
from models.llama_loader import client, MODEL_NAME

def score_vocabulary(text: str) -> dict:
    if not text.strip():
        return {"score": 100, "flagged": [], "machine_translated": False, "mode": "offline_empty_guard"}

    sliced_text = text[:1500]

    system_prompt = (
        "You are an expert philologist, lexicographer, and computational linguist specializing in the Bulgarian language.\n"
        "Your objective is to evaluate the provided Bulgarian text for lexical authenticity and vocabulary naturalness.\n\n"
        "Look precisely for:\n"
        "1. Unnecessary loanwords/foreign borrowings (чуждици) where perfectly natural Bulgarian alternatives exist.\n"
        "2. Structural or semantic calques (калки) resulting from literal word-for-word translations from English or Russian.\n"
        "3. Non-idiomatic expressions that sound unnatural or forced to a native Bulgarian speaker.\n"
        "4. Overarching linguistic footprints or repetitive patterns that point directly to an automated Machine Translation (MT) engine output.\n\n"
        "CRITICAL INSTRUCTION: You must respond ONLY with a single valid JSON object matching the exact schema below. "
        "Do not prefix or append any introductions, explanations, markdown code fences (like ```json), or backticks outside the raw JSON code.\n\n"
        "Expected JSON Output Schema:\n"
        "{\n"
        "  \"score\": <integer from 0 to 100 representing lexical authenticity and quality>,\n"
        "  \"flagged\": [\n"
        "    {\n"
        "      \"phrase\": \"the unnatural or foreign phrase flagged in the text\",\n"
        "      \"reason\": \"clear explanation of why this phrase is non-authentic or flawed, written in English\",\n"
        "      \"suggestion\": \"the natural, authentic native Bulgarian substitute phrase or word\"\n"
        "    }\n"
        "  ],\n"
        "  \"machine_translated\": <true|false boolean flag if the text shows clear signs of automated machine translation>\n"
        "}"
    )

    user_payload = f"Analyze the vocabulary authenticity of this Bulgarian text:\n\"\"\"\n{sliced_text}\n\"\"\""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_payload}
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=800,
            temperature=0.1,
            seed=42
        )
        
        raw_content = response.choices[0].message.content.strip()
        
        json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if json_match:
            parsed_json = json.loads(json_match.group())
            parsed_json["mode"] = "cloud_llama_vocabulary"
            return parsed_json
            
        return {
            "score": 50, 
            "flagged": [], 
            "machine_translated": False, 
            "mode": "json_parse_fallback",
            "error": "Failed to extract valid JSON layout boundaries from model string stream response."
        }

    except Exception as e:
        return {
            "score": 50, 
            "flagged": [], 
            "machine_translated": False, 
            "mode": "runtime_exception_fallback",
            "error": f"Internal vocabulary analyzer processing crash: {str(e)}"
        }