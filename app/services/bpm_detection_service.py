import aubio
import numpy as np


class BPMDetector:
    def __init__(self):
        pass

    def detect_bpm(self, audio_path):
        # Setup aubio's tempo detection
        win_s = 512  # Window size
        hop_s = win_s // 2  # Hop size
        s = aubio.source(audio_path, samplerate=0, hop_size=hop_s)
        samplerate = s.samplerate
        o = aubio.tempo("default", win_s, hop_s, samplerate)

        # List to collect detected beats
        beats = []

        # Process the audio file
        total_frames = 0
        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                beats.append(o.get_last_s())
            total_frames += read
            if read < hop_s: break

        # Calculate BPM
        if len(beats) > 1:
            bpms = 60. / np.diff(beats)
            bpm = np.median(bpms)
        else:
            bpm = 0

        return bpm


def bpm_detection(file_path):
    # Assuming you've already set up your BPMDetector class in bpm_detection_service.py
    detector = BPMDetector()
    bpm = detector.detect_bpm(file_path)
    return bpm
