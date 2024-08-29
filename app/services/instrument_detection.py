import torch
import torchaudio
import openunmix
from openunmix import predict
import librosa


def detect_instruments(audio_file_path):
    # Load the audio file
    audio, sr = librosa.load(audio_file_path, sr=44100, mono=False)

    # Convert the audio to a tensor
    audio_tensor = torch.tensor(audio).unsqueeze(0)  # Add batch dimension

    # Load the pre-trained Open Unmix model
    model = openunmix.umxhq()  # Use a variant of Open Unmix

    # Perform the prediction
    estimates = predict.separate(model, audio_tensor)

    # Analyze the estimates to detect instruments
    detected_instruments = []
    if torch.mean(estimates['bass']) > 0.1:  # Example threshold
        detected_instruments.append('bass')
    if torch.mean(estimates['drums']) > 0.1:
        detected_instruments.append('drums')
    if torch.mean(estimates['vocals']) > 0.1:
        detected_instruments.append('vocals')
    if torch.mean(estimates['other']) > 0.1:
        detected_instruments.append('other instruments')

    return detected_instruments


# if __name__ == "__main__":
#     audio_file_path = "/mnt/data/kk_mere_mehboob.mp3"
#     instruments = detect_instruments(audio_file_path)
#     print("Detected instruments:", instruments)
