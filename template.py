import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    ".github/workflows/.gitkeep",
    "main.py",
    "pipeline.py",
    "config.py",
    ".env",
    "requirements.txt",
    "setup.sh",
    "README.md",
    "ingestion/__init__.py",
    "ingestion/document_reader.py",
    "ingestion/audio_transcriber.py",
    "detection/__init__.py",
    "detection/lang_detector.py",
    "models/__init__.py",
    "models/bggpt_loader.py",
    "models/whisper_loader.py",
    "models/hf_api_client.py",
    "dimensions/__init__.py",
    "dimensions/grammar.py",
    "dimensions/vocabulary.py",
    "dimensions/fluency.py",
    "dimensions/spelling.py",
    "dimensions/register.py",
    "scoring/__init__.py"
]




for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")                                                                    