import crepe
import librosa
import numpy as np
import essentia.standard as es

class MelodyChordsDetector:
    def __init__(self):
        pass

    def detect_melody(self, audio_path):
        # Load the audio file
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Use CREPE to predict the melody (pitch) over time
        time, frequency, confidence, activation = crepe.predict(y, sr, viterbi=True)
        
        # Convert frequency to MIDI notes
        midi_notes = librosa.hz_to_midi(frequency)
        
        # Filter out low-confidence predictions
        melody = midi_notes[confidence > 0.5]

        return melody, time

    def detect_chords(self, audio_path):
        # Load the audio file
        loader = es.MonoLoader(filename=audio_path)
        audio = loader()
        
        # Compute the predominant pitch
        pitch_extractor = es.PredominantPitchMelodia()
        pitch, _ = pitch_extractor(audio)
        
        # Compute the HPCP chroma (requires multiple inputs, such as pitch and audio)
        hpcp = es.HPCP()
        hpcp_output = hpcp(pitch)  # Provide the necessary arguments
        
        # Detect chords using the HPCP output
        chord_extractor = es.ChordsDetection()
        chords, _ = chord_extractor(hpcp_output)

        return chords

    def extract_melody_chords(self, audio_path):
        melody, time = self.detect_melody(audio_path)
        chords = self.detect_chords(audio_path)
                # Ensure the output is a dictionary
        melody_chords = {
            'melody': melody,
            'time': time,
            'chords': chords
        }
        return melody_chords


def melody_chords_detection(file_path):
    # Assuming you've already set up your MelodyChordsDetector class in melody_chords_detection_service.py
    detector = MelodyChordsDetector()
    melody_chords = detector.extract_melody_chords(file_path)
    return melody_chords
