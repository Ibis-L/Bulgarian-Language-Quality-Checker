import os
import json
from analyzer import analyze_bulgarian_text
from ingestion.audio_transcriber import transcribe_audio
from ingestion.document_reader import extract_text

def process_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found: {file_path}"}

    ext = os.path.splitext(file_path)[1].lower()
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a']
    doc_extensions = ['.txt', '.pdf', '.docx']

    if ext in audio_extensions:
        transcription_result = transcribe_audio(file_path)
        if "error" in transcription_result:
            return {"status": "error", "message": transcription_result["error"]}
            
        extracted_text = transcription_result.get("text", "").strip()
        return analyze_bulgarian_text(extracted_text)

    elif ext in doc_extensions:
        try:
            extracted_text = extract_text(file_path).strip()
            if not extracted_text:
                return {"status": "error", "message": "The extracted document is empty or unreadable."}
                
            return analyze_bulgarian_text(extracted_text)
        except Exception as e:
            return {"status": "error", "message": f"Extraction crash: {str(e)}"}

    else:
        return {
            "status": "error", 
            "message": f"Unsupported file type '{ext}'. Please provide audio ({', '.join(audio_extensions)}) or documents ({', '.join(doc_extensions)})."
        }

if __name__ == "__main__":
   
    test_file = input("Enter the path to your file (audio or document): ").strip()
    report = process_file(test_file)
    print("\nFINAL REPORT: ")
    print(json.dumps(report, indent=2, ensure_ascii=False))