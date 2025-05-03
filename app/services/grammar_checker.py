from vertexai.language_models import TextGenerationModel
import vertexai
from config import Config

class GrammarChecker:
    def __init__(self):
        vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
        self.model = TextGenerationModel.from_pretrained(Config.MODEL_NAME)


    def check(self, text: str) -> str:
        prompt = f"Aşağıdaki metindeki yazım ve dil bilgisi hatalarını açıkla:\n\n{text}"
        response = self.model.predict(prompt, temperature=0.2, max_output_tokens=1024)
        return response.text.strip()
