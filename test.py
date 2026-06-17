# from ingestion.document_reader import extract_text
# from detection.lang_detector import detect_language

# data = extract_text("./test.txt")

# analysis = detect_language(data)

# print(analysis)

# test.py

# # test.py
# import json
# from analyzer import analyze_bulgarian_text

# def run_test_case(label: str, text: str):

#     print(f"TEST CASE: {label}")
#     print(f"Input Text: '{text[:100]}...'")
  
#     report = analyze_bulgarian_text(text)
    
#     print(json.dumps(report, indent=2, ensure_ascii=False))

# if __name__ == "__main__":
#     valid_bulgarian = (
#         "Вчера отидох до магазина и си купих хляб. "
#         "Времето беше изключително хубаво и се разходих в парка."
#     )
#     run_test_case("Valid Bulgarian Input", valid_bulgarian)
    
   
#     flawed_bulgarian = (
#         "Той влезе във магазина без да каже нищо. "
#         "Това беше една много хубавоо и приятна вечер."
#     )
#     run_test_case("Flawed Bulgarian Input", flawed_bulgarian)

#     english_text = "Hello world! This pipeline should halt immediately and refuse to process this."
#     run_test_case("Non-Bulgarian Safety Filter Guard", english_text)
# test_audio.py
import os
import json
from ingestion.audio_transcriber import transcribe_audio
from analyzer import analyze_bulgarian_text

def run_audio_pipeline_test(audio_filename: str):

    root_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(root_dir, audio_filename)
    
    if not os.path.exists(audio_path):
        print(f"Error: Test audio file '{audio_filename}' not found.")
        return

    transcription_result = transcribe_audio(audio_path)
    
    if "error" in transcription_result:
        print(f"Transcription Failure: {transcription_result['error']}")
        print(json.dumps(transcription_result, indent=2))
        return

    extracted_text = transcription_result.get("text", "").strip()
    print(f"Transcription Success!")
    print(f"Generated Transcript Text: \"{extracted_text}\"")
   

   
    print("Step 2: Feeding text transcript into the 5-Dimension Linguistic Analyzer...")
    analysis_report = analyze_bulgarian_text(extracted_text)

    
    print("\nFINAL REPORT]")
    print(json.dumps(analysis_report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    TARGET_TEST_FILE = "test_input.mp3"
    run_audio_pipeline_test(TARGET_TEST_FILE)