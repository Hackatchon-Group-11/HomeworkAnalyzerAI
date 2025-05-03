# app/analyzer.py
from app.services.file_reader import FileReader
from app.services.text_cleaner import TextCleaner
from app.services.grammar_checker import GrammarChecker
from app.services.topic_detector import TopicDetector
from app.services.recommendation_engine import RecommendationEngine

class HomeworkAnalyzer:
    def __init__(self, file_path: str, filetype: str):
        self.file_path = file_path
        self.filetype = filetype
        self.reader = FileReader()
        self.cleaner = TextCleaner()
        self.grammar = GrammarChecker()
        self.detector = TopicDetector()
        self.recommender = RecommendationEngine()

    def analyze(self):
        raw_text = self.reader.read(self.file_path, self.filetype)
        clean_text = self.cleaner.clean(raw_text)
        grammar_issues = self.grammar.check(raw_text)
        found_topics = self.detector.detect(clean_text)
        suggestions = self.recommender.recommend(found_topics)

        return {
            "bulunan_konular": found_topics,
            "eksik_konular": suggestions,
            "gramer_hatalari": grammar_issues
        }
