import subprocess
import os

def generate_voiceover(script, filename="voiceover.mp3"):
    temp_filename = "temp_voiceover.aiff"

    # Using the say command to create the AIFF file
    say_command = ['say', '-o', temp_filename, script]
    try:
        subprocess.run(say_command, check=True)
    except subprocess.CalledProcessError:
        print("Failed to generate the AIFF file with 'say'.")
        return None

    # Check if the AIFF file was created
    if not os.path.exists(temp_filename):
        print("AIFF file was not created.")
        return None

    # Convert AIFF to MP3 using ffmpeg
    ffmpeg_command = ['ffmpeg', '-y', '-i', temp_filename, '-codec:a', 'libmp3lame', filename]
    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError:
        print("FFmpeg failed to convert AIFF to MP3.")
        return None

    # Check if the MP3 file was created
    if not os.path.exists(filename):
        print("MP3 file was not created.")
        return None

    # Remove the temporary AIFF file
    os.remove(temp_filename)

    return filename
