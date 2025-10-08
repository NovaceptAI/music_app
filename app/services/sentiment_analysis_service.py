from app.services.azure_openai_service import azure_openai_service


class SentimentAnalysisService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def analyze_sentiment(self, lyrics):
        """
        Analyze sentiment of lyrics
        
        Args:
            lyrics (str): The lyrics to analyze
            
        Returns:
            dict: Sentiment analysis result
        """
        try:
            sentiment = self.openai_service.analyze_sentiment(lyrics)
            
            return {
                "original_lyrics": lyrics,
                "sentiment_analysis": sentiment,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Sentiment analysis failed: {str(e)}",
                "status": "error"
            }

    def analyze_melody_sentiment(self, melody_features):
        """
        Analyze sentiment from melody features
        
        Args:
            melody_features (dict): Musical features of the melody
            
        Returns:
            dict: Melody sentiment analysis result
        """
        try:
            sentiment = self.openai_service.analyze_melody_sentiment(melody_features)
            
            return {
                "melody_features": melody_features,
                "sentiment_analysis": sentiment,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Melody sentiment analysis failed: {str(e)}",
                "status": "error"
            }


def analyze_sentiment(lyrics):
    """Service function for lyrics sentiment analysis"""
    service = SentimentAnalysisService()
    return service.analyze_sentiment(lyrics)


def analyze_melody_sentiment(melody_features):
    """Service function for melody sentiment analysis"""
    service = SentimentAnalysisService()
    return service.analyze_melody_sentiment(melody_features)
