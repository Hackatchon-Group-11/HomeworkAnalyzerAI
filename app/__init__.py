from flask import Flask
from flasgger import Swagger
from app.router.homework_ai_router import routes
from config import Config
import vertexai

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)

    app.register_blueprint(routes)

    swagger_config = {
        "headers": [],
        "title": "Homework AI API",
        "version": "1.0.0",
        "description": "Ödev analiz servisi.",
        "termsOfService": "",
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ]
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Homework AI API",
            "description": "Bu API, eğitim amaçlı ödev dosyalarının analizini sağlar.",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    return app
