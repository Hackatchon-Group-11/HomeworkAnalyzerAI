from vertexai.language_models import TextGenerationModel
from config import Config
import json
import os

class TopicDetector:
    def __init__(self):
        self.model = TextGenerationModel.from_pretrained(Config.MODEL_NAME)

        with open(Config.CONTENT_JSON_PATH, "r", encoding="utf-8") as f:
            self.konular = [k["konu"] for k in json.load(f)]

    def detect(self, text: str) -> list:
        prompt = f"""Metindeki konuları aşağıdaki listeden seç:
{', '.join(self.konular)}

Metin:
{text}

Sadece ilgili konuları madde halinde yaz:"""

        try:
            response = self.model.predict(
                prompt,
                temperature=0.2,
                max_output_tokens=512
            )
            return [line.strip("-• ") for line in response.text.strip().splitlines() if line.strip()]
        except Exception as e:
            print(f"[Vertex AI Error] {e}")
            return []
