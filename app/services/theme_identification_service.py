from app.services.azure_openai_service import azure_openai_service


class ThemeIdentificationService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def identify_themes(self, lyrics):
        """
        Identify themes in lyrics
        
        Args:
            lyrics (str): The lyrics to analyze
            
        Returns:
            dict: Theme identification result
        """
        try:
            themes = self.openai_service.identify_themes(lyrics)
            
            return {
                "original_lyrics": lyrics,
                "themes": themes,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Theme identification failed: {str(e)}",
                "status": "error"
            }


def identify_themes(lyrics):
    """Service function for theme identification"""
    service = ThemeIdentificationService()
    return service.identify_themes(lyrics)
