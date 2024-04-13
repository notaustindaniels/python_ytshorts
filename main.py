from dotenv import load_dotenv
import os
from scripts.input_processing import get_video_idea
from scripts.script_generation import generate_script
from scripts.voiceover_generation import generate_voiceover
from scripts.timestamp_subtitle_generation import generate_subtitles
from scripts.image_generation import generate_images
from scripts.video_concatenation import create_video

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def main():
    video_idea = get_video_idea()
    script = generate_script(video_idea, API_KEY)
    audio_file = generate_voiceover(script)
    text, segments = generate_subtitles(audio_file, API_KEY)
    sentences = [seg['text'] for seg in segments]
    images = generate_images(sentences, API_KEY)
    create_video(images, audio_file, sentences)

if __name__ == "__main__":
    main()
