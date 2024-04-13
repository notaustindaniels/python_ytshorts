import pyttsx3

def generate_voiceover(script, filename="voiceover.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(script, filename)
    engine.runAndWait()
    return filename
