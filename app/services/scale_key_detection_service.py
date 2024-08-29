import librosa.feature
import numpy as np


class ScaleKeyDetector:
    def __init__(self):
        pass

    def detect_scale_key(self, audio_path):
        # Load the audio file
        y, sr = librosa.load(audio_path)

        # Compute the chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Compute the chroma feature vector mean (aggregate chroma values over time)
        chroma_mean = np.mean(chroma, axis=1)

        # Define a heuristic to estimate the key
        # For simplicity, we can use the index of the highest chroma feature as an approximation for the key
        key_index = np.argmax(chroma_mean)

        # Map the key index to a musical key (C, C#, D, ..., B)
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key = keys[key_index]

        # Simple heuristic to guess the scale (major or minor)
        # This heuristic is not perfect and may require adjustment
        if key_index in [0, 2, 4, 5, 7, 9, 11]:  # C, D, E, F, G, A, B (major keys)
            scale = 'major'
        else:
            scale = 'minor'

        return {'key': key, 'scale': scale}


def scale_key_detection(file_path):
    # Assuming you've already set up your ScaleKeyDetector class in scale_key_detection_service.py
    detector = ScaleKeyDetector()
    scale_key = detector.detect_scale_key(file_path)
    return scale_key
