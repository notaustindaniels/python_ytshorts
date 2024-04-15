import os
from dotenv import load_dotenv
from scripts.input_processing import process_input
from scripts.script_generation import generate_script
from scripts.voiceover_generation import generate_voiceover
from scripts.timestamp_subtitle_generation import generate_subtitles
from scripts.image_generation import generate_images
from scripts.video_concatenation import concatenate_video
from scripts.burn_subtitles import burn_subtitles

def main():
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
    
    video_idea = process_input()
    script = generate_script(video_idea, openai_key)
    voiceover_file = generate_voiceover(script)
    subtitles_file = generate_subtitles(assemblyai_key, voiceover_file)
    images = generate_images(script, openai_key)
    video_file = concatenate_video(images, voiceover_file)
    final_video = burn_subtitles(video_file, subtitles_file)

    print("Video creation complete:", final_video)

if __name__ == "__main__":
    main()
