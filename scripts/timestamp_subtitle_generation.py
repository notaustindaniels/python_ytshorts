import assemblyai
import os

def generate_subtitles(api_key, filename="voiceover.mp3"):
    assemblyai.api_key = api_key

    # Create a transcriber object and transcribe the audio file
    transcript = assemblyai.Transcriber().transcribe(filename)
    subtitles = transcript.export_subtitles_srt()

    # Save subtitles to file
    with open("subtitles.srt", "w") as f:
        f.write(subtitles)

    return "subtitles.srt"
