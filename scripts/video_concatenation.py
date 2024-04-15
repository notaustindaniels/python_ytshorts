from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips

def concatenate_video(images, audio_filename):
    clip = ImageSequenceClip(images, fps=1)  # 1 frame per second
    audio = AudioFileClip(audio_filename)
    final_clip = clip.set_audio(audio)
    final_clip.write_videofile("final_video.mp4", codec="libx264")

    return "final_video.mp4"
