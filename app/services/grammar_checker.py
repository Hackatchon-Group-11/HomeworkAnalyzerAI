from vertexai.language_models import TextGenerationModel
from config import Config

class GrammarChecker:
    def __init__(self):
        self.model = TextGenerationModel.from_pretrained(Config.MODEL_NAME)

    def check(self, text: str) -> str:
        prompt = f"Aşağıdaki metinde bulunan yazım ve dil bilgisi hatalarını belirle ve her hata için doğru hâlini yaz:\n\n{text}"
        response = self.model.predict(prompt, temperature=0.2, max_output_tokens=1024)
        return response.text.strip()
