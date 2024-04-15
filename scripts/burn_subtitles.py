from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip

def burn_subtitles(video_filename, subtitles_filename):
    video = VideoFileClip(video_filename)
    subtitles = TextClip(subtitles_filename, fontsize=24, color='white')
    subtitles = subtitles.set_position(('center', 'bottom')).set_duration(video.duration)

    final_video = CompositeVideoClip([video, subtitles])
    final_video.write_videofile("final_video_with_subtitles.mp4", codec="libx264")

    return "final_video_with_subtitles.mp4"
