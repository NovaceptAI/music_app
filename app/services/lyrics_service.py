import os
import azure.cognitiveservices.speech as speechsdk


class LyricsExtractor:
    def __init__(self, subscription_key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    def extract_lyrics_from_audio(self, audio_path):
        audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        transcription = []

        def handle_final_result(evt):
            transcription.append(evt.result.text)

        speech_recognizer.recognized.connect(handle_final_result)
        speech_recognizer.start_continuous_recognition()
        speech_recognizer.stop_continuous_recognition()

        return " ".join(transcription)


def lyrics_extraction(file_path):
    # Assuming you've already set up your LyricsExtractor class in lyrics_service.py
    extractor = LyricsExtractor(subscription_key="00c46faca1434597ac942d9f661ed77f", region="eastus")
    return extractor.extract_lyrics_from_audio(file_path)

