from dotenv import load_dotenv
import os
import json

from scripts.input_processing import process_input
from scripts.script_generation import generate_script
from scripts.voiceover_generation import generate_voiceover
from scripts.timestamp_subtitle_generation import generate_subtitles
from scripts.image_segment_generator.select_segments import select_segments
from scripts.image_segment_generator.generate_prompts import generate_prompts
from scripts.image_segment_generator.generate_images import generate_images
from scripts.video_concatenation import concatenate_video
from scripts.burn_subtitles import burn_subtitles

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

    if not OPENAI_API_KEY or not ASSEMBLYAI_API_KEY:
        print("API keys are not set correctly.")
        return

    video_idea = process_input()
    script = generate_script(video_idea, OPENAI_API_KEY)
    if not script:
        print("Script generation failed.")
        return

    script_filename = 'script.txt'
    with open(script_filename, 'w', encoding='utf-8') as file:
        file.write(script)

    voiceover_filename = generate_voiceover(script)
    if not voiceover_filename:
        print("Voiceover generation failed.")
        return

    subtitle_filename = generate_subtitles(ASSEMBLYAI_API_KEY, voiceover_filename)
    if not subtitle_filename:
        print("Subtitle generation failed.")
        return

    segments = select_segments(script_filename, subtitle_filename, OPENAI_API_KEY)
    if not segments:
        print("Segment selection failed.")
        return

    prompts = generate_prompts(segments, OPENAI_API_KEY)
    images = generate_images(prompts, OPENAI_API_KEY)
    if not images:
        print("Image generation failed.")
        return

    final_video = concatenate_video(images, subtitle_filename, voiceover_filename)
    if not final_video:
        print("Video concatenation failed.")
        return

    final_video_with_subtitles = burn_subtitles(final_video, subtitle_filename)
    if not final_video_with_subtitles:
        print("Subtitle burning failed.")
        return

if __name__ == '__main__':
    main()
