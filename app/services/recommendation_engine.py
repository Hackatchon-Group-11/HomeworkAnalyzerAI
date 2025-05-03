from config import Config
import json

class RecommendationEngine:
    def __init__(self):
        with open(Config.CONTENT_JSON_PATH, "r", encoding="utf-8") as f:
            self.content = json.load(f)

    def recommend(self, found_topics: list) -> list:
        all_topics = [item["konu"] for item in self.content]
        missing = set(all_topics) - set(found_topics)
        return [item for item in self.content if item["konu"] in missing]
