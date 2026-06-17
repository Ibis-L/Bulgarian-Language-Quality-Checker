from langdetect import detect_langs
from langdetect import DetectorFactory

DetectorFactory.seed = 0

def detect_language(text: str) -> dict:
    if not text.strip():
        return {"language": "unknown", "confidence": 0.0, "is_bulgarian": False}

    try:
        sample_text = text[:512]
        
        predictions = detect_langs(sample_text)
        best_match = predictions[0]
        
        lang_code = best_match.lang
        confidence = round(best_match.prob * 100, 1)
        
        return {
            "language": lang_code,
            "confidence": confidence,
            "is_bulgarian": lang_code == "bg",
            "mode": "offline_pure_python"
        }
    except Exception as e:
        return {
            "language": "error",
            "confidence": 0.0,
            "is_bulgarian": False,
            "error": f"Detection failed: {str(e)}"
        }