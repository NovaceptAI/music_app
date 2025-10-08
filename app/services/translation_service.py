from app.services.azure_openai_service import azure_openai_service


class TranslationService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def translate_lyrics(self, lyrics, target_language):
        """
        Translate lyrics to target language
        
        Args:
            lyrics (str): The lyrics to translate
            target_language (str): Target language (e.g., 'Spanish', 'French', 'German')
            
        Returns:
            dict: Translation result with original and translated text
        """
        try:
            translated_lyrics = self.openai_service.translate_lyrics(lyrics, target_language)
            
            return {
                "original_lyrics": lyrics,
                "translated_lyrics": translated_lyrics,
                "target_language": target_language,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Translation failed: {str(e)}",
                "status": "error"
            }


def translate_lyrics(lyrics, target_language="English"):
    """Service function for lyrics translation"""
    service = TranslationService()
    return service.translate_lyrics(lyrics, target_language)
