from dotenv import load_dotenv
import os
import json

# Import custom scripts
from scripts.input_processing import process_input
from scripts.script_generation import generate_script
from scripts.voiceover_generation import generate_voiceover
from scripts.timestamp_subtitle_generation import generate_subtitles
from scripts.image_segment_generator.select_segments import select_segments
from scripts.image_segment_generator.assign_durations import assign_durations
from scripts.image_segment_generator.generate_prompts import generate_prompts
from scripts.image_segment_generator.generate_images import generate_images
from scripts.video_concatenation import concatenate_video
from scripts.burn_subtitles import burn_subtitles

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

    video_idea = process_input()
    script = generate_script(video_idea, OPENAI_API_KEY)

    script_filename = 'script.txt'
    with open(script_filename, 'w', encoding='utf-8') as file:
        file.write(script)

    voiceover_filename = generate_voiceover(script)
    subtitle_filename = generate_subtitles(ASSEMBLYAI_API_KEY, voiceover_filename)

    segments = select_segments(script_filename, subtitle_filename, OPENAI_API_KEY)
    durations = assign_durations(segments)
    durations_file = 'durations.json'
    with open(durations_file, 'w') as f:
        json.dump(durations, f)

    prompts = generate_prompts(segments)
    images = generate_images(prompts, OPENAI_API_KEY)

    final_video = concatenate_video(images, durations_file, voiceover_filename)
    final_video_with_subtitles = burn_subtitles(final_video, subtitle_filename)

if __name__ == '__main__':
    main()
