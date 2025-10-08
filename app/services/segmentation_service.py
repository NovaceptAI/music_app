from app.services.azure_openai_service import azure_openai_service


class SegmentationService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def segment_lyrics(self, lyrics):
        """
        Segment lyrics into structural parts (verse, chorus, bridge, etc.)
        
        Args:
            lyrics (str): The lyrics to segment
            
        Returns:
            dict: Segmentation result
        """
        try:
            segments = self.openai_service.segment_lyrics(lyrics)
            
            return {
                "original_lyrics": lyrics,
                "segments": segments,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Lyrics segmentation failed: {str(e)}",
                "status": "error"
            }


def segment_lyrics(lyrics):
    """Service function for lyrics segmentation"""
    service = SegmentationService()
    return service.segment_lyrics(lyrics)
