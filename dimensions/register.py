import re
import json
from models.llama_loader import client, MODEL_NAME

def score_register(text: str) -> dict:
    if not text.strip():
        return {"score": 100, "dominant_register": "unknown", "inconsistencies": [], "mode": "offline_empty_guard"}

    sliced_text = text[:1500]

    system_prompt = (
        "You are an expert Bulgarian sociolinguist, style editor, and copywriter.\n"
        "Your task is to analyze the provided Bulgarian text for stylistic register consistency.\n\n"
        "Linguistic Evaluation Criteria:\n"
        "1. Identify the dominant register: 'formal' (официално-делови), 'informal' (разговорен), or 'mixed'.\n"
        "2. Check for incorrect pronoun capitalization. In formal Bulgarian, the polite form 'Вие' (You), 'Ваш' (Your), "
        "and 'Си' must be capitalized when addressing an individual. Lowercase 'вие' indicates standard plural or informal slip-ups.\n"
        "3. Watch out for jarring stylistic clashes, such as using street slang or highly casual phrases within an otherwise formal business letter.\n"
        "4. Flag any inconsistencies where the text shifts uncomfortably between formal and informal tones without a logical transition.\n\n"
        "CRITICAL INSTRUCTION: You must respond ONLY with a single valid JSON object matching the exact schema below. "
        "Do not include any prefaces, wrapping text, markdown code blocks, or backticks outside the raw JSON code.\n\n"
        "Expected JSON Output Schema:\n"
        "{\n"
        "  \"score\": <integer from 0 to 100 tracking register consistency and correctness>,\n"
        "  \"dominant_register\": \"formal|informal|mixed\",\n"
        "  \"inconsistencies\": [\n"
        "    {\n"
        "      \"sentence\": \"the specific sentence string where the stylistic clash occurs\",\n"
        "      \"issue\": \"clear explanation of the register clash or pronoun error in English\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    user_payload = f"Analyze the stylistic register of this Bulgarian text:\n\"\"\"\n{sliced_text}\n\"\"\""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_payload}
    ]

    try:
        
        response = client.chat_completion(
            messages=messages,
            max_tokens=600,
            temperature=0.1, 
            seed=42
        )
        
        raw_content = response.choices[0].message.content.strip()
        
        json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if json_match:
            parsed_json = json.loads(json_match.group())
            parsed_json["mode"] = "cloud_llama_register"
            return parsed_json
            
        return {
            "score": 70,
            "dominant_register": "unknown",
            "inconsistencies": [],
            "mode": "json_parse_fallback",
            "error": "Failed to isolate valid JSON boundaries from model response stream."
        }

    except Exception as e:
        return {
            "score": 70,
            "dominant_register": "unknown",
            "inconsistencies": [],
            "mode": "runtime_exception_fallback",
            "error": f"Internal register analyzer processing crash: {str(e)}"
        }