# app/services/text_cleaner.py
import re
import spacy

nlp = spacy.load("xx_ent_wiki_sm")

class TextCleaner:
    def clean(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def lemmatize(self, text: str) -> str:
        doc = nlp(text)
        return " ".join(token.lemma_ for token in doc)
