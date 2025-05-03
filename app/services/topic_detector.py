from vertexai.language_models import TextGenerationModel
import vertexai
from config import Config
import json

class TopicDetector:
    def __init__(self):
        vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
        self.model = TextGenerationModel.from_pretrained("gemini-1.5-pro-preview-0409")
        with open(Config.CONTENT_JSON_PATH, "r", encoding="utf-8") as f:
            self.konular = [k["konu"] for k in json.load(f)]

    def detect(self, text: str):
        prompt = f"""
Metindeki konuları aşağıdaki listeden seç:
{', '.join(self.konular)}

Metin:
{text}

Liste halinde sadece ilgili konuları yaz.
"""
        try:
            response = self.model.predict(prompt, temperature=0.2, max_output_tokens=512)
        except Exception as e:
            print(f"[Vertex AI Error] {e}")
            return "Dil kontrolü yapılamadı."
        return [line.strip("-• ") for line in response.text.strip().splitlines() if line.strip()]
