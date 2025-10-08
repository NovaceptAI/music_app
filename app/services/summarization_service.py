from app.services.azure_openai_service import azure_openai_service


class SummarizationService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def summarize_lyrics(self, lyrics, summary_type="comprehensive"):
        """
        Summarize lyrics content
        
        Args:
            lyrics (str): The lyrics to summarize
            summary_type (str): 'comprehensive' or 'short'
            
        Returns:
            dict: Summarization result
        """
        try:
            summary = self.openai_service.summarize_lyrics(lyrics, summary_type)
            
            return {
                "original_lyrics": lyrics,
                "summary": summary,
                "summary_type": summary_type,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Summarization failed: {str(e)}",
                "status": "error"
            }


def summarize_lyrics(lyrics, summary_type="comprehensive"):
    """Service function for lyrics summarization"""
    service = SummarizationService()
    return service.summarize_lyrics(lyrics, summary_type)
