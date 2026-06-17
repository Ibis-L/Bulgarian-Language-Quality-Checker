In this project we made a Bulgarian Language Quality Checker.
It consist of 3 parts:
1>Ingestion  2>Language Detection  3>Score Calculation

1>Ingestion:
Here I make sure to get the text from the document, to get text from audio, whisper model is used

2>Langauge Detection:
langdetect is used to detect the language, it is a machine learning or more like a statiscal model that use ngram in order to check the most often comming words or pair of charaters in the languages and give percantage of it being to that particular language

3>Scoring:
In scoring, in order to calculatescore for grammer, vocabulary, fluency, register consistency I used the llama model deployed on hugging face and as for thr spelling score I used spelling checking against the Bulgarian Dictionary, checking the words that are not present

Then in analyzer we calculate the complete score using the formula = grammar_score*0.30 + vocabulary_score*0.25 + fluency_score*0.20 + spelling_score*0.15 + register_score*0.10

Scope of improvement:
In pdfs using OCR and use of more stronger models with more parameters like XLM-Roberta for language detection instead of just matching, we can also calcul;ate fluency use perplexity formula => e^Loss

We can run this file by importing the functins from main.py