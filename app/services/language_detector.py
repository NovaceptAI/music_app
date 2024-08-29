from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class LanguageDetector:
    def __init__(self, endpoint, key):
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def detect_language(self, text):
        response = self.client.detect_language(documents=[{"id": "1", "text": text}])[0]
        language = response.primary_language.iso6391_name
        return language
