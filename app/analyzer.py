from app.services.file_reader import FileReader
from app.services.text_cleaner import TextCleaner
from app.services.grammar_checker import GrammarChecker
from app.services.topic_detector import TopicDetector
from app.services.recommendation_engine import RecommendationEngine
from app.services.question_answer_analyzer import QuestionAnswerAnalyzer

class HomeworkAnalyzer:
    def __init__(self, file_path: str, filetype: str):
        self.file_path = file_path
        self.filetype = filetype
        self.reader = FileReader()
        self.cleaner = TextCleaner()
        self.grammar = GrammarChecker()
        self.detector = TopicDetector()
        self.recommender = RecommendationEngine()
        self.qa_analyzer = QuestionAnswerAnalyzer()
        self.chunk_size = 8000  # karakter bazlı parça limiti

    def _split_text(self, text: str, max_chars: int = 8000) -> list:
        """Uzun metni parçalar (token limiti için)."""
        return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

    def analyze(self) -> dict:
        raw_text = self.reader.read(self.file_path, self.filetype)
        clean_text = self.cleaner.clean(raw_text)


        grammar_issues = []
        for chunk in self._split_text(raw_text):
            grammar_issues += self.grammar.check(chunk)


        found_topics = self.detector.detect(clean_text)
        suggestions = self.recommender.recommend(found_topics)


        qa_analysis = []
        for chunk in self._split_text(raw_text):
            qa_analysis += self.qa_analyzer.analyze_qa_pairs(chunk)

        return {
            "bulunan_konular": found_topics,
            "eksik_konular": suggestions,
            "gramer_hatalari": grammar_issues,
            "soru_cevap_analizi": qa_analysis
        }
