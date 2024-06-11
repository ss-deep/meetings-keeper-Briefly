from moviepy.editor import VideoFileClip
import subprocess
from faster_whisper import WhisperModel
import os
import speech_recognition as sr

def video_to_audio(video_path, output_audio_path):
    """ Convert a video to audio and save it to the output path.
    Parameters: video_path (str): The path to the video file.
    output_audio_path (str): The path to save the audio to. """
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio.write_audiofile(output_audio_path)

def audio_to_text(audio_path):
    """ Convert audio to text using the SpeechRecognition library.
    Parameters: audio_path (str): The path to the audio file.
    Returns: test (str): The text recognized from the audio. """
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)

    with audio as source:
        # Record the audio data
        audio_data = recognizer.record(source)

        try:
            # Recognize the speech
            text = recognizer.recognize_whisper(audio_data)
        except sr.UnknownValueError:
            print("Speech recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from service; {e}")

    return text
