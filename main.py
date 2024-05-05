from dotenv import load_dotenv
import os
import json

from scripts.input_processing import process_inputs
from scripts.timestamp_subtitle_generation import generate_subtitles
from scripts.image_segment_generator.select_segments import select_segments
from scripts.image_segment_generator.assign_durations import assign_durations
from scripts.image_segment_generator.generate_prompts import generate_prompts
from scripts.image_segment_generator.generate_images import generate_images
from scripts.video_processing.video_concatenation import concatenate_video
from scripts.burn_subtitles import burn_subtitles

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

    if not OPENAI_API_KEY or not ASSEMBLYAI_API_KEY:
        print("API keys are not set correctly.")
        return

    audio_filepath, script_filepath = process_inputs()
    if not os.path.exists(audio_filepath) or not os.path.exists(script_filepath):
        print("Audio file or script file does not exist.")
        return

    voiceover_filename = audio_filepath  # Since the voiceover is already provided

    subtitle_filename = generate_subtitles(ASSEMBLYAI_API_KEY, voiceover_filename)
    if not subtitle_filename:
        print("Subtitle generation failed.")
        return
    else:
        print("Subtitle generation successful.")

    segments = select_segments(script_filepath, subtitle_filename, OPENAI_API_KEY)
    if not segments:
        print("Segment selection failed.")
        return
    else:
        print("Segment selection successful.")

    durations = assign_durations(segments)
    durations_file = 'durations.json'
    with open(durations_file, 'w') as f:
        json.dump(durations, f)
        print("Durations assigned and saved.")

    prompts = generate_prompts(segments, OPENAI_API_KEY)
    images = generate_images(prompts, OPENAI_API_KEY)
    if not images:
        print("Image generation failed.")
        return
    else:
        print("Images generated successfully.")

    final_video = concatenate_video(images, durations_file, voiceover_filename)
    if not final_video:
        print("Video concatenation failed.")
        return
    else:
        print("Video concatenation successful.")

    final_video_with_subtitles = burn_subtitles(final_video, subtitle_filename)
    if not final_video_with_subtitles:
        print("Subtitle burning failed.")
        return
    else:
        print("Subtitles burned into video successfully.")

if __name__ == '__main__':
    main()