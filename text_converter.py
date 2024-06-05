from utils import video_to_audio, audio_to_text
import os
from groq_api import summary_generator

def video_to_text_converter(video_file):
    try:
        filepath=f"./uploads/{video_file}"
        output_video_path = "./video_data/"
        output_folder = "./uploads/"
        output_audio_path = "./uploads/audio/converted_to_audio.wav"

        # video_to_images(filepath, output_folder)
        video_to_audio(filepath, output_audio_path)
        text_data = audio_to_text(output_audio_path)

        #store transcript in the txt file
        with open(output_folder + "transcript.txt", "w") as file:
            file.write(text_data)

        # calling Groq Api to summarize video text
        summary_data=summary_generator(text_data)

        #store summary in the txt file
        with open(output_folder + "summary.txt", "w") as file:
            file.write(summary_data)

        print("Text data saved to file")
        # file.close()
        os.remove(output_audio_path)
        print("Audio file removed")

    except Exception as e:
        raise e
    
