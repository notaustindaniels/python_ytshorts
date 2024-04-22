from scripts.input_processing import process_audio_input, process_script_input
# Other imports remain the same

def main():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

    if not OPENAI_API_KEY or not ASSEMBLYAI_API_KEY:
        print("API keys are not set correctly.")
        return

    # Obtain audio file path and script file path from user input
    audio_file_path = process_audio_input()
    script_file_path = process_script_input()

    # Generate subtitles directly from the user-provided voiceover
    subtitle_filename = generate_subtitles(ASSEMBLYAI_API_KEY, audio_file_path)
    if not subtitle_filename:
        print("Subtitle generation failed.")
        return

    # Use the provided script file path directly for segment selection
    segments = select_segments(script_file_path, subtitle_filename, OPENAI_API_KEY)
    if not segments:
        print("Segment selection failed.")
        return

    durations = assign_durations(segments)
    durations_file = 'durations.json'
    with open(durations_file, 'w') as f:
        json.dump(durations, f)

    prompts = generate_prompts(segments, OPENAI_API_KEY)
    images = generate_images(prompts, OPENAI_API_KEY)
    if not images:
        print("Image generation failed.")
        return

    final_video = concatenate_video(images, durations_file, audio_file_path)
    if not final_video:
        print("Video concatenation failed.")
        return

    final_video_with_subtitles = burn_subtitles(final_video, subtitle_filename)
    if not final_video_with_subtitles:
        print("Subtitle burning failed.")
        return

if __name__ == '__main__':
    main()
