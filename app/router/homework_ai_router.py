from flask import Blueprint, request, jsonify, send_file
from flasgger import swag_from
from app.services.file_reader import FileReader
from app.services.text_cleaner import TextCleaner
from app.services.grammar_checker import GrammarChecker
from app.services.topic_detector import TopicDetector
from app.services.recommendation_engine import RecommendationEngine
from app.services.question_answer_analyzer import QuestionAnswerAnalyzer
from app.analyzer import HomeworkAnalyzer

import mimetypes
from tempfile import NamedTemporaryFile

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET"])
@swag_from({
    'tags': ['General'],
    'responses': {
        200: {'description': 'API çalışıyor'}
    }
})
def home():
    return "Homework Analyzer API is running!"

@routes.route("/analyze", methods=["POST"])
@swag_from({
    'tags': ['Analyze'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Yüklenen ödev dosyası'
        },
        {
            'name': 'type',
            'in': 'formData',
            'type': 'string',
            'enum': ['pdf', 'docx', 'txt'],
            'required': True,
            'description': 'Dosya türü'
        },
        {
            'name': 'format',
            'in': 'formData',
            'type': 'string',
            'enum': ['json', 'pdf', 'docx', 'md'],
            'required': False,
            'description': 'Çıktı formatı (varsayılan json)'
        }
    ],
    'responses': {
        200: {
            'description': 'Analiz başarılı',
        },
        400: {
            'description': 'Eksik parametre'
        }
    }
})
def analyze_homework():
    file = request.files.get("file")
    filetype = request.form.get("type")
    output_format = request.form.get("format", "json")

    if not file or not filetype:
        return jsonify({"error": "File and type are required"}), 400

    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    analyzer = HomeworkAnalyzer(temp_path, filetype)
    result = analyzer.analyze()

    if output_format == "json":
        return jsonify(result)

    qa_list = result["soru_cevap_analizi"]
    temp_file = NamedTemporaryFile(delete=False, suffix=f".{output_format}")
    output_path = temp_file.name

    if output_format == "pdf":
        analyzer.qa_analyzer.to_pdf(qa_list, output_path)
    elif output_format == "docx":
        analyzer.qa_analyzer.to_docx(qa_list, output_path)
    elif output_format == "md":
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(analyzer.qa_analyzer.to_markdown(qa_list))
    else:
        return jsonify({"error": "Unsupported format"}), 400

    return send_file(output_path, as_attachment=True, mimetype=mimetypes.guess_type(output_path)[0])


@routes.route("/read", methods=["POST"])
@swag_from({
    'tags': ['Read'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Dosya içeriğini okur'
        },
        {
            'name': 'type',
            'in': 'formData',
            'type': 'string',
            'enum': ['pdf', 'docx', 'txt'],
            'required': True,
            'description': 'Dosya türü'
        }
    ],
    'responses': {
        200: {'description': 'Okunan metin döner'}
    }
})
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
@swag_from({
    'tags': ['Clean'],
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {'text': {'type': 'string'}}
            }
        }
    ],
    'responses': {
        200: {'description': 'Temizlenmiş ve lemmatize edilmiş metin'}
    }
})
def clean_text():
    data = request.get_json()
    text = data.get("text", "")

    cleaner = TextCleaner()
    cleaned = cleaner.clean(text)
    lemmatized = cleaner.lemmatize(text)

    return jsonify({"cleaned": cleaned, "lemmatized": lemmatized})


@routes.route("/grammar", methods=["POST"])
@swag_from({
    'tags': ['Grammar'],
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {'text': {'type': 'string'}}
            }
        }
    ],
    'responses': {
        200: {'description': 'Dil bilgisi hataları'}
    }
})
def grammar_check():
    data = request.get_json()
    text = data.get("text", "")

    checker = GrammarChecker()
    issues = checker.check(text)

    return jsonify({"grammar_issues": issues})


@routes.route("/topics", methods=["POST"])
@swag_from({
    'tags': ['Topics'],
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {'text': {'type': 'string'}}
            }
        }
    ],
    'responses': {
        200: {'description': 'Tespit edilen konular'}
    }
})
def detect_topics():
    data = request.get_json()
    text = data.get("text", "")

    cleaner = TextCleaner()
    clean_text = cleaner.clean(text)

    detector = TopicDetector()
    topics = detector.detect(clean_text)

    return jsonify({"topics": topics})


@routes.route("/recommend", methods=["POST"])
@swag_from({
    'tags': ['Recommend'],
    'parameters': [
        {
            'name': 'topics',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {'topics': {'type': 'array', 'items': {'type': 'string'}}}
            }
        }
    ],
    'responses': {
        200: {'description': 'Tavsiye edilen içerikler'}
    }
})
def recommend_content():
    data = request.get_json()
    found_topics = data.get("topics", [])

    recommender = RecommendationEngine()
    suggestions = recommender.recommend(found_topics)

    return jsonify({"recommendations": suggestions})


@routes.route("/qa-analyze", methods=["POST"])
@swag_from({
    'tags': ['QA Analyze'],
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {'text': {'type': 'string'}}
            }
        }
    ],
    'responses': {
        200: {'description': 'Soru-cevap analizi sonucu'}
    }
})
def qa_analysis():
    data = request.get_json()
    text = data.get("text", "")

    analyzer = QuestionAnswerAnalyzer()
    results = analyzer.analyze_qa_pairs(text)

    return jsonify({"qa_analysis": results})
