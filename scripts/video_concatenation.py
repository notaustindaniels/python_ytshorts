from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video(images, audio_file, subtitles, output_file="output_video.mp4"):
    clips = []
    audio_clip = AudioFileClip(audio_file)
    for i, (image_path, subtitle) in enumerate(zip(images, subtitles)):
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration / len(images))
        text_clip = TextClip(subtitle, fontsize=24, color='white').set_position('bottom').set_duration(image_clip.duration)
        clips.append(CompositeVideoClip([image_clip, text_clip]))
    final_clip = concatenate_videoclips(clips).set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec='libx264')
