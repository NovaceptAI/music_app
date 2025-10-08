from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


class LanguageDetector:
    def __init__(self, endpoint="https://scoolish-text-analytics.cognitiveservices.azure.com/", key=None):
        if key is None:
            # Key should be provided via environment variable or config
            raise ValueError("Azure Text Analytics key must be provided")
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def detect_language(self, text):
        """
        Detect language of given text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Language detection result
        """
        try:
            response = self.client.detect_language(documents=[{"id": "1", "text": text}])[0]
            language = response.primary_language.iso6391_name
            confidence = response.primary_language.confidence_score
            
            return {
                "text": text,
                "detected_language": language,
                "confidence": confidence,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Language detection failed: {str(e)}",
                "status": "error"
            }


def detect_language(text):
    """Service function for language detection"""
    # You should pass the actual key from config or environment variable
    detector = LanguageDetector(key="YOUR_AZURE_TEXT_ANALYTICS_KEY")
    return detector.detect_language(text)
