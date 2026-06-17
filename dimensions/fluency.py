import re
import json
from models.llama_loader import client, MODEL_NAME

def score_fluency(text: str) -> dict:
    if not text.strip():
        return {"score": 100, "perplexity_proxy": 1.0, "feedback": "Empty text provided.", "mode": "offline_empty_guard"}

    sliced_text = text[:1500]

    system_prompt = (
        "You are an expert style editor and computational linguist native to Bulgaria.\n"
        "Your task is to score the fluency, sentence transition flow, phrasing rhythm, "
        "and general naturalness of the provided Bulgarian text.\n\n"
        "Evaluate the text on a scale from 0 to 100:\n"
        "- 90 to 100: Exceptional, elegant flow, native-level phrasing and seamless sentence transitions.\n"
        "- 70 to 89: Normal conversational text, fully comprehensible but slightly rigid or modern informal.\n"
        "- 40 to 69: Awkward phrasing, heavy repetition, choppy sentences, or clear text artifact errors.\n"
        "- 0 to 39: Fragmented clauses, broken syntactic ordering, or incomprehensible garbage text.\n\n"
        "You must also output a calculated 'perplexity_proxy' representing text chaos:\n"
        "- Highly natural text should map to a lower proxy score (between 10.0 and 40.0).\n"
        "- Extremely robotic or fragmented text should map to a higher proxy score (above 150.0).\n\n"
        "CRITICAL INSTRUCTION: You must respond ONLY with a single valid JSON object matching the exact schema below. "
        "Do not include any conversational prose, prefaces, summary write-ups, or backticks outside the raw JSON code.\n\n"
        "Expected JSON Output Schema:\n"
        "{\n"
        "  \"score\": <integer from 0 to 100 representing fluency flow>,\n"
        "  \"perplexity_proxy\": <float tracking flow chaos, typically 10.0 to 250.0>,\n"
        "  \"feedback\": \"a single concise sentence in English summarizing the rhythm and readability flaws\"\n"
        "}"
    )

    user_payload = f"Analyze the structural fluency of this Bulgarian text:\n\"\"\"\n{sliced_text}\n\"\"\""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_payload}
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=500,
            temperature=0.1, 
            seed=42
        )
        
        raw_content = response.choices[0].message.content.strip()
        
        
        json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if json_match:
            parsed_json = json.loads(json_match.group())
            parsed_json["perplexity_proxy"] = round(float(parsed_json.get("perplexity_proxy", 50.0)), 2)
            parsed_json["mode"] = "cloud_llama_fluency"
            return parsed_json
            
        return {
            "score": 50, 
            "perplexity_proxy": 100.0, 
            "feedback": "Failed to parse valid JSON layout boundaries from model response stream.",
            "mode": "json_parse_fallback"
        }

    except Exception as e:
        return {
            "score": 50, 
            "perplexity_proxy": 100.0, 
            "feedback": f"Internal fluency processing exception: {str(e)}",
            "mode": "runtime_exception_fallback"
        }