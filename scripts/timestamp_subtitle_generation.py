import assemblyai
import os
import srt_equalizer

def generate_subtitles(api_key, filename="voiceover.mp3"):
    assemblyai.api_key = api_key

    # Create a transcriber object and transcribe the audio file
    transcript = assemblyai.Transcriber().transcribe(filename)
    subtitles = transcript.export_subtitles_srt()

    # Save original subtitles to a temporary file
    temp_srt_path = "temp_subtitles.srt"
    with open(temp_srt_path, "w") as f:
        f.write(subtitles)

    # Equalize the subtitles
    equalize_subtitles(temp_srt_path, "subtitles.srt", max_chars=10)

    return "subtitles.srt"

def equalize_subtitles(input_srt_path: str, output_srt_path: str, max_chars: int = 10) -> None:
    """
    Adjust subtitles to have a maximum number of characters per line using srt_equalizer.

    Args:
        input_srt_path (str): Path to the input SRT file.
        output_srt_path (str): Path to the output SRT file.
        max_chars (int): Maximum number of characters per subtitle line.
    """
    # Using the srt_equalizer to adjust subtitle line length
    srt_equalizer.equalize_srt_file(input_srt_path, output_srt_path, max_chars, method='greedy')

