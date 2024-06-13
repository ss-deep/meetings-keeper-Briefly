from utils import video_to_audio, audio_to_text
import os
from pydub import AudioSegment

def video_to_text_converter(file):
    try:
        filepath = f"./uploads/{file}"
        output_audio_path = "./uploads/converted_to_audio.wav"
        extention = file.split('.').pop()
        
        print(f"Processing file: {filepath}")
        print(f"Extension: {extention}")

        if extention in ['mp4', 'mov', 'avi']:
            # Convert uploaded video file to audio
            video_to_audio(filepath, output_audio_path)
            text_data = audio_to_text(output_audio_path)
        elif extention in ['mp3', 'wav', 'm4a']:
            if extention == 'mp3':
                sound = AudioSegment.from_mp3(filepath)  # Use filepath instead of file
                sound.export(output_audio_path, format="wav")
            elif extention == 'm4a':
                sound = AudioSegment.from_file(filepath, format='m4a')
                sound.export(output_audio_path, format="wav")
            else:
                output_audio_path = filepath
            text_data = audio_to_text(output_audio_path)

        print("Text data saved to file")
        os.remove(output_audio_path)
        os.remove(filepath)
        print("Audio and video files removed")
        return text_data

    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
        raise fnf_error
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
