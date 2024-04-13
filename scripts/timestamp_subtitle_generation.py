import openai

def generate_subtitles(audio_file, api_key):
    openai.api_key = api_key
    response = openai.Audio.transcribe(
        model="whisper-large",
        file=open(audio_file, "rb")
    )
    return response['text'], response['segments']
