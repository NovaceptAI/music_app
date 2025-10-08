from app.services.azure_openai_service import azure_openai_service


class KeywordExtractionService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def extract_keywords(self, lyrics):
        """
        Extract keywords from lyrics
        
        Args:
            lyrics (str): The lyrics to analyze
            
        Returns:
            dict: Keyword extraction result
        """
        try:
            keywords = self.openai_service.extract_keywords(lyrics)
            
            return {
                "original_lyrics": lyrics,
                "keywords": keywords,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Keyword extraction failed: {str(e)}",
                "status": "error"
            }


def extract_keywords(lyrics):
    """Service function for keyword extraction"""
    service = KeywordExtractionService()
    return service.extract_keywords(lyrics)
