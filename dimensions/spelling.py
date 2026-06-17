import os
import re
from spellchecker import SpellChecker

DICTIONARY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bg.json.gz")

def score_spelling(text: str) -> dict:
    if not text.strip():
        return {"score": 100, "total_words": 0, "misspelled_count": 0, "misspelled": [], "mode": "pyspellchecker_compiled_dict"}

    words = re.findall(r'[а-яА-ЯѝъЪьЬѣѢѫѪ]+', text.lower())

    if not words:
        return {"score": 100, "total_words": 0, "misspelled_count": 0, "misspelled": [], "mode": "pyspellchecker_compiled_dict"}

    try:
        if not os.path.exists(DICTIONARY_PATH):
            return {
                "score": 100, "total_words": len(words), "misspelled_count": 0, "misspelled": [],
                "mode": "spelling_asset_missing",
                "error": f"Dictionary file missing. Please run compile_dict.py to generate it at: {DICTIONARY_PATH}"
            }

        spell = SpellChecker(language=None, local_dictionary=DICTIONARY_PATH)
        
        misspelled = list(spell.unknown(words))
        error_rate = len(misspelled) / len(words)
        score = max(0, int((1 - error_rate) * 100))
        
        return {
            "score": score,
            "total_words": len(words),
            "misspelled_count": len(misspelled),
            "misspelled": list(set(misspelled))[:20],
            "mode": "pyspellchecker_compiled_dict"
        }
        
    except Exception as e:
        return {
            "score": 100, "total_words": len(words), "misspelled_count": 0, "misspelled": [],
            "mode": "spelling_runtime_exception",
            "error": str(e)
        }