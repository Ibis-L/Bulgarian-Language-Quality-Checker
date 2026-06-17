import re
import json
from models.llama_loader import client, MODEL_NAME

def score_grammar(text: str) -> dict:
    if not text.strip():
        return {"score": 100, "issues": [], "mode": "offline_empty_guard"}

    sliced_text = text[:1500]

    system_prompt = (
        "You are an expert Bulgarian language schoolteacher and elite grammarian.\n"
        "Your task is to analyze the user's provided Bulgarian text for syntax errors, "
        "verb conjugation inconsistencies, case issues, definite article mismatches (пълен/кратък член), "
        "and general grammatical slip-ups.\n\n"
        "CRITICAL INSTRUCTION: You must respond ONLY with a single valid JSON object matching the exact schema below. "
        "Do not include any introductory phrases, wrap headers, conversational commentary, or formatting markdown blocks outside the raw JSON code.\n\n"
        "Expected JSON Output Schema:\n"
        "{\n"
        "  \"score\": <integer from 0 to 100 representing grammatical correctness>,\n"
        "  \"issues\": [\n"
        "    {\n"
        "      \"sentence\": \"the exact text string fragment where the mistake occurs\",\n"
        "      \"error\": \"clear explanation of the grammatical error written in concise English\",\n"
        "      \"severity\": \"low|medium|high\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )

    user_payload = f"Analyze this Bulgarian text:\n\"\"\"\n{sliced_text}\n\"\"\""

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
            parsed_json["mode"] = "cloud_llama_grammar"
            return parsed_json
        
        return {
            "score": 50, 
            "issues": [], 
            "mode": "json_parse_fallback",
            "error": "Failed to extract valid JSON layout boundaries from model string stream response."
        }

    except Exception as e:
        return {
            "score": 50, 
            "issues": [], 
            "mode": "runtime_exception_fallback",
            "error": f"Internal grammar analyzer processing crash: {str(e)}"
        }