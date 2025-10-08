import openai
import random
import json
from tenacity import retry, wait_exponential, stop_after_attempt
from app.config.config import Config


class AzureOpenAIService:
    def __init__(self):
        self.api_keys = Config.AZURE_OPENAI_API_KEYS
        self.api_bases = Config.AZURE_OPENAI_API_BASES
        self.deployment = Config.AZURE_OPENAI_DEPLOYMENT
        self.current_key_index = 0
        
        # Validate configuration
        if not self.api_keys or not self.api_bases:
            raise ValueError("Azure OpenAI API keys and bases must be configured via environment variables")
        
        if len(self.api_keys) != len(self.api_bases):
            raise ValueError("Number of API keys must match number of API bases")

    def _get_current_client(self):
        """Get the current Azure OpenAI client with rotation support"""
        api_key = self.api_keys[self.current_key_index]
        api_base = self.api_bases[self.current_key_index]
        
        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_version = "2024-02-15-preview"
        
        return openai

    def _rotate_key(self):
        """Rotate to the next API key"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def _make_request(self, messages, temperature=0.7, max_tokens=1500):
        """Make a request to Azure OpenAI with retry logic"""
        try:
            client = self._get_current_client()
            response = client.ChatCompletion.create(
                engine=self.deployment,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            self._rotate_key()
            raise e

    def translate_lyrics(self, lyrics, target_language):
        """Translate lyrics to target language"""
        messages = [
            {"role": "system", "content": "You are a professional translator specializing in song lyrics. Preserve the poetic nature and emotional tone while translating accurately."},
            {"role": "user", "content": f"Translate the following lyrics to {target_language}. Maintain the original structure and emotional tone:\n\n{lyrics}"}
        ]
        return self._make_request(messages)

    def summarize_lyrics(self, lyrics, summary_type="comprehensive"):
        """Summarize lyrics based on type (comprehensive/short)"""
        if summary_type == "comprehensive":
            prompt = f"Provide a comprehensive summary of the following song lyrics, including main themes, emotional journey, and key messages:\n\n{lyrics}"
        else:
            prompt = f"Provide a short, concise summary of the main theme and message in these lyrics:\n\n{lyrics}"
        
        messages = [
            {"role": "system", "content": "You are a music analyst specializing in lyrical content analysis."},
            {"role": "user", "content": prompt}
        ]
        return self._make_request(messages)

    def identify_themes(self, lyrics):
        """Identify themes in lyrics"""
        messages = [
            {"role": "system", "content": "You are a literary analyst specializing in song lyrics. Identify and categorize themes present in the text."},
            {"role": "user", "content": f"Analyze the following lyrics and identify all major themes. Return the result as a JSON array of themes with confidence scores:\n\n{lyrics}"}
        ]
        response = self._make_request(messages)
        
        try:
            # Try to parse as JSON, fallback to text if it fails
            return json.loads(response)
        except:
            return {"themes": response, "format": "text"}

    def extract_keywords(self, lyrics):
        """Extract significant keywords from lyrics"""
        messages = [
            {"role": "system", "content": "You are a text analysis expert. Extract the most significant keywords and phrases from song lyrics."},
            {"role": "user", "content": f"Extract the most important keywords and phrases from these lyrics. Return as a JSON array with keywords and their relevance scores:\n\n{lyrics}"}
        ]
        response = self._make_request(messages)
        
        try:
            return json.loads(response)
        except:
            return {"keywords": response, "format": "text"}

    def segment_lyrics(self, lyrics):
        """Segment lyrics into verses, chorus, bridge, etc."""
        messages = [
            {"role": "system", "content": "You are a music structure analyst. Identify and label different sections of song lyrics (verse, chorus, bridge, etc.)."},
            {"role": "user", "content": f"Analyze these lyrics and segment them into structural parts (verse, chorus, bridge, pre-chorus, outro, etc.). Return the result with clear labels:\n\n{lyrics}"}
        ]
        return self._make_request(messages)

    def analyze_sentiment(self, lyrics):
        """Analyze sentiment of lyrics"""
        messages = [
            {"role": "system", "content": "You are a sentiment analysis expert specializing in music and lyrics. Provide detailed emotional analysis."},
            {"role": "user", "content": f"Analyze the sentiment and emotional content of these lyrics. Provide overall sentiment, emotional intensity, and specific emotions identified:\n\n{lyrics}"}
        ]
        return self._make_request(messages)

    def classify_genre(self, audio_features=None, lyrics=None):
        """Classify genre based on audio features and/or lyrics"""
        content_parts = []
        
        if lyrics:
            content_parts.append(f"Lyrics:\n{lyrics}")
        
        if audio_features:
            content_parts.append(f"Audio Features:\n{json.dumps(audio_features, indent=2)}")
        
        if not content_parts:
            return {"error": "No input provided for genre classification"}
        
        content = "\n\n".join(content_parts)
        
        messages = [
            {"role": "system", "content": "You are a music genre classification expert. Analyze the provided information to determine the most likely genre and subgenre."},
            {"role": "user", "content": f"Based on the following information, classify the genre and subgenre of this music. Provide confidence scores:\n\n{content}"}
        ]
        return self._make_request(messages)

    def analyze_melody_sentiment(self, melody_features):
        """Analyze sentiment from melody features"""
        messages = [
            {"role": "system", "content": "You are a music theory expert specializing in melody analysis and emotional interpretation."},
            {"role": "user", "content": f"Analyze the emotional content and sentiment of this melody based on its musical features:\n\n{json.dumps(melody_features, indent=2)}\n\nProvide sentiment analysis with emotional descriptors and intensity scores."}
        ]
        return self._make_request(messages)


# Singleton instance
azure_openai_service = AzureOpenAIService()
