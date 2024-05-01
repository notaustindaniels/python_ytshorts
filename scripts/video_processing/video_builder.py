from moviepy.editor import concatenate_videoclips, AudioFileClip
import os

def build_video(clips, voiceover_filename, output_file="final_video.mp4"):
    if not os.path.isfile(voiceover_filename):
        print(f"Audio file not found: {voiceover_filename}")
        return None

    audio_clip = AudioFileClip(voiceover_filename)
    print(f"Loaded audio file with duration: {audio_clip.duration} seconds")

    if not clips:
        print("No video clips were created.")
        return None

    video_clip = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)

    # Ensure the final clip extends to the end of the audio if necessary
    final_end_time = max(clips[-1].end, audio_clip.duration)
    extended_last_clip = clips[-1].set_end(final_end_time)
    clips[-1] = extended_last_clip

    video_clip.write_videofile(output_file, fps=30, threads=2)
    print(f"Video creation complete, file saved to: {output_file}")
    return output_file
