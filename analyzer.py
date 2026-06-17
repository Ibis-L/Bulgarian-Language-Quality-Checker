import time
from detection.lang_detector import detect_language
from dimensions.grammar import score_grammar 
from dimensions.fluency import  score_fluency 
from dimensions.register import score_register 
from dimensions.spelling import score_spelling 
from dimensions.vocabulary import score_vocabulary     
from ingestion.audio_transcriber import transcribe_audio

def compute_bulgarity_score(dim_scores: dict) -> float:
    weights = {
        "grammar":    0.30,
        "vocabulary": 0.25,
        "fluency":    0.20,
        "spelling":   0.15,
        "register":   0.10
    }
    
    total = sum(dim_scores.get(dim, 50) * w for dim, w in weights.items())
    return round(total, 1)

def analyze_bulgarian_text(text: str) -> dict:
    start_time = time.time()
    
    lang_metrics = detect_language(text)
    is_confident_bg = lang_metrics["is_bulgarian"] and lang_metrics["confidence"] >= 70.0
    
    if not (is_confident_bg):
        return {
            "status": "rejected",
            "reason": f"Input language verification failed. Detected: {lang_metrics['language'].upper()}",
            "metrics": lang_metrics
        }
        
    print("Language verified. Computing Score")
    
    grammar_res = score_grammar(text)
    vocab_res = score_vocabulary(text)
    fluency_res = score_fluency(text)
    spelling_res = score_spelling(text)
    register_res = score_register(text)
    
    extracted_scores = {
        "grammar":    grammar_res.get("score", 50),
        "vocabulary": vocab_res.get("score", 50),
        "fluency":    fluency_res.get("score", 50),
        "spelling":   spelling_res.get("score", 50),
        "register":   register_res.get("score", 50)
    }
    
    final_score = compute_bulgarity_score(extracted_scores)
    execution_time = round(time.time() - start_time, 2)
    
    return {
        "status": "success",
        "final_bulgarity_score": final_score,
        "execution_time_sec": execution_time,
        "dimension_breakdown": {
            "grammar": grammar_res,
            "vocabulary": vocab_res,
            "fluency": fluency_res,
            "spelling": spelling_res,
            "register": register_res
        }
    }

def process_audio_pipeline(audio_file_path: str):
    transcription_result = transcribe_audio(audio_file_path)
    
    if "error" in transcription_result:
        return transcription_result
        
    print("Transcription complete. Passing text to Bulgariantool Analyzer...")
    return analyze_bulgarian_text(transcription_result["text"])