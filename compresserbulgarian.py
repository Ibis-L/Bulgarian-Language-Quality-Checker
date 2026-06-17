import urllib.request
import os
from spellchecker import SpellChecker

def build_enterprise_dictionary():
    url = "https://raw.githubusercontent.com/titoBouzout/Dictionaries/master/Bulgarian.dic"
   
    
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Download failed: {e}")
        return

 
    clean_words = []
    
   
    for line in data.splitlines()[1:]:
        word = line.split('/')[0].strip()
        if word:
            clean_words.append(word.lower())

   
    temp_txt_path = "bulgarian_words_large.txt"
    with open(temp_txt_path, "w", encoding="utf-8") as f:
        f.write(" ".join(clean_words))

    
    spell = SpellChecker(language=None)
    spell.word_frequency.load_text_file(temp_txt_path)
    spell.export("bg.json.gz", gzipped=True)
    
    if os.path.exists(temp_txt_path):
        os.remove(temp_txt_path)
        
    print("Success")

if __name__ == "__main__":
    build_enterprise_dictionary()