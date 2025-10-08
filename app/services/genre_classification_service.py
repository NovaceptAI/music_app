from app.services.azure_openai_service import azure_openai_service
import librosa
import numpy as np


class GenreClassificationService:
    def __init__(self):
        self.openai_service = azure_openai_service

    def extract_audio_features(self, audio_path):
        """
        Extract audio features for genre classification
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Audio features
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path)
            
            # Extract various features
            features = {
                "tempo": float(librosa.beat.tempo(y=y, sr=sr)[0]),
                "spectral_centroid": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
                "spectral_rolloff": float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))),
                "zero_crossing_rate": float(np.mean(librosa.feature.zero_crossing_rate(y))),
                "mfcc": np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1).tolist(),
                "chroma": np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1).tolist(),
                "spectral_contrast": np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1).tolist(),
                "tonnetz": np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr), axis=1).tolist()
            }
            
            return features
        except Exception as e:
            return {"error": f"Feature extraction failed: {str(e)}"}

    def classify_genre(self, audio_path=None, lyrics=None, audio_features=None):
        """
        Classify genre based on audio features and/or lyrics
        
        Args:
            audio_path (str): Path to audio file (optional)
            lyrics (str): Song lyrics (optional)
            audio_features (dict): Pre-extracted audio features (optional)
            
        Returns:
            dict: Genre classification result
        """
        try:
            # Extract audio features if path provided and features not given
            if audio_path and not audio_features:
                audio_features = self.extract_audio_features(audio_path)
                if "error" in audio_features:
                    return audio_features
            
            # Classify genre using OpenAI
            genre_result = self.openai_service.classify_genre(audio_features, lyrics)
            
            return {
                "audio_features": audio_features,
                "lyrics": lyrics,
                "genre_classification": genre_result,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": f"Genre classification failed: {str(e)}",
                "status": "error"
            }


def classify_genre(audio_path=None, lyrics=None, audio_features=None):
    """Service function for genre classification"""
    service = GenreClassificationService()
    return service.classify_genre(audio_path, lyrics, audio_features)
