from flask import Blueprint, request, jsonify
from app.services.file_reader import FileReader
from app.services.text_cleaner import TextCleaner
from app.services.grammar_checker import GrammarChecker
from app.services.topic_detector import TopicDetector
from app.services.recommendation_engine import RecommendationEngine
from app.services.question_answer_analyzer import QuestionAnswerAnalyzer
from app.analyzer import HomeworkAnalyzer

routes = Blueprint("routes", __name__)

@routes.route("/analyze", methods=["POST"])
def analyze_homework():
    file = request.files.get("file")
    filetype = request.form.get("type")  # 'pdf' or 'docx'

    if not file or not filetype:
        return jsonify({"error": "File and type are required"}), 400

    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    analyzer = HomeworkAnalyzer(temp_path, filetype)
    result = analyzer.analyze()

    return jsonify(result)


@routes.route("/read", methods=["POST"])
def read_file():
    file = request.files.get("file")
    filetype = request.form.get("type")

    if not file or not filetype:
        return jsonify({"error": "File and type are required"}), 400

    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    reader = FileReader()
    text = reader.read(temp_path, filetype)

    return jsonify({"text": text})


@routes.route("/clean", methods=["POST"])
def clean_text():
    data = request.get_json()
    text = data.get("text", "")

    cleaner = TextCleaner()
    cleaned = cleaner.clean(text)
    lemmatized = cleaner.lemmatize(text)

    return jsonify({"cleaned": cleaned, "lemmatized": lemmatized})


@routes.route("/grammar", methods=["POST"])
def grammar_check():
    data = request.get_json()
    text = data.get("text", "")

    checker = GrammarChecker()
    issues = checker.check(text)

    return jsonify({"grammar_issues": issues})


@routes.route("/topics", methods=["POST"])
def detect_topics():
    data = request.get_json()
    text = data.get("text", "")

    cleaner = TextCleaner()
    clean_text = cleaner.clean(text)

    detector = TopicDetector()
    topics = detector.detect(clean_text)

    return jsonify({"topics": topics})


@routes.route("/recommend", methods=["POST"])
def recommend_content():
    data = request.get_json()
    found_topics = data.get("topics", [])

    recommender = RecommendationEngine()
    suggestions = recommender.recommend(found_topics)

    return jsonify({"recommendations": suggestions})


@routes.route("/qa-analyze", methods=["POST"])
def qa_analysis():
    data = request.get_json()
    text = data.get("text", "")

    analyzer = QuestionAnswerAnalyzer()
    results = analyzer.analyze_qa_pairs(text)

    return jsonify({"qa_analysis": results})
