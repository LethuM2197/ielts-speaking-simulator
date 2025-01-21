import os
import wave
from google.cloud import speech_v1
from google.cloud import storage


def process_audio(audio_file_path):
    """
    Process an audio file and return its transcription using Google Cloud Speech-to-Text API.

    Parameters:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Transcription of the audio file, or None if an error occurs.
    """
    try:
        # Validate the audio file format
        if not os.path.isfile(audio_file_path):
            raise FileNotFoundError(f"File not found: {audio_file_path}")

        # Open and check the audio file using the wave module
        with wave.open(audio_file_path, 'rb') as wave_file:
            channels = wave_file.getnchannels()
            sample_width = wave_file.getsampwidth()
            frame_rate = wave_file.getframerate()
            duration = wave_file.getnframes() / float(frame_rate)

        if channels > 1:
            raise ValueError("Audio file must be mono (single channel).")
        if sample_width != 2:  # 2 bytes per sample for LINEAR16
            raise ValueError("Audio file must use 16-bit samples.")
        if frame_rate not in [8000, 16000, 44100]:
            raise ValueError(f"Unexpected sample rate: {frame_rate}")

        # Initialize the Speech-to-Text client
        client = speech_v1.SpeechClient()

        # Read the audio file's content
        with open(audio_file_path, 'rb') as audio_file:
            content = audio_file.read()

        # Configure the recognition settings
        audio = speech_v1.RecognitionAudio(content=content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=frame_rate,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        # Perform the transcription
        response = client.recognize(config=config, audio=audio)

        # Extract the transcribed text
        transcription = " ".join(result.alternatives[0].transcript for result in response.results)

        return transcription.strip()

    except FileNotFoundError as fnf_error:
        print(f"File error: {str(fnf_error)}")
        return None
    except ValueError as val_error:
        print(f"Audio validation error: {str(val_error)}")
        return None
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        return None
