import assemblyai
import os

def ms_to_srt_time(ms):
    """Convert milliseconds to SRT time format."""
    hours = ms // 3600000
    ms = ms % 3600000
    minutes = ms // 60000
    ms = ms % 60000
    seconds = ms // 1000
    milliseconds = ms % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_subtitles(api_key, filename="voiceover.mp3"):
    assemblyai.api_key = api_key

    # Create a transcriber object and transcribe the audio file
    transcriber = assemblyai.Transcriber()
    transcript = transcriber.transcribe(filename)

    # Generate SRT from word timestamps
    subtitles = []
    for index, word in enumerate(transcript.words, start=1):
        start_time = ms_to_srt_time(word.start)
        end_time = ms_to_srt_time(word.end)
        subtitles.append(f"{index}\n{start_time} --> {end_time}\n{word.text}\n")

    # Save subtitles to a file
    srt_path = "subtitles.srt"
    with open(srt_path, "w") as f:
        f.write("\n".join(subtitles))

    return srt_path
