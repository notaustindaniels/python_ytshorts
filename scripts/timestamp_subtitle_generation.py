import assemblyai
import os
import srt_equalizer

def generate_subtitles(api_key, filename="voiceover.mp3"):
    client = assemblyai.Client(api_key=api_key)  # Initialize the API client with your API key

    # Upload the audio file and get the URL
    audio_url = client.upload(filename=filename)

    # Request transcription of the uploaded audio file, enabling word timestamps
    transcript = client.transcribe(audio_url=audio_url, word_timestamps=True)

    # Check the status of the transcription until it's complete
    while transcript['status'] != 'completed':
        transcript = client.get_transcript(transcript['id'])
        time.sleep(5)  # Pause the loop for 5 seconds before checking again

    # Export the completed transcription to SRT format
    subtitles = client.export_transcript(transcript['id'], format='srt')

    # Save the subtitles to a file
    output_srt_path = "subtitles.srt"
    with open(output_srt_path, "w") as f:
        f.write(subtitles)

    return output_srt_path