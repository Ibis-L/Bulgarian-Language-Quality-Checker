import argparse
import json
import sys
import os

from analyzer import analyze_bulgarian_text, process_audio_pipeline

def main():
    parser = argparse.ArgumentParser(description="Bulgarian Language Quality Checker")
    parser.add_argument("--file", required=True, help="Path to document (.txt) or audio file")
    parser.add_argument("--output", default="report.json", help="Output JSON file path")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found -> {args.file}")
        sys.exit(1)

    print(f"Analyzing: {args.file}")

    file_ext = os.path.splitext(args.file)[1].lower()
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']

    if file_ext in audio_extensions:
        report = process_audio_pipeline(args.file)
    else:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text_content = f.read()
            report = analyze_bulgarian_text(text_content)
        except Exception as e:
            report = {"error": f"Failed to read text file: {str(e)}"}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    if "error" in report:
        print(f"\nPipeline Error: {report['error']}")
    elif report.get("status") == "rejected":
        print(f"\nAnalysis Rejected: {report.get('reason')}")
    else:
        score = report.get('final_bulgarity_score', 'N/A')
        print(f"\nBulgarity Score: {score}/100")
        
    print(f"Full report saved to: {args.output}")

if __name__ == "__main__":
    main()