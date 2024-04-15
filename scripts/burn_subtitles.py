from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip

def make_subtitle_clip(txt, fontsize=100, color='yellow', font='./fonts/bold_font.ttf'):
    # Helper function to style subtitles
    return TextClip(txt, fontsize=fontsize, color=color, font=font, stroke_color='black', stroke_width=5, method='caption')

def burn_subtitles(video_filename, subtitles_filename):
    video = VideoFileClip(video_filename)
    # Set video to 30fps
    video = video.set_fps(30)

    # Generate subtitles clip
    subtitles = SubtitlesClip(subtitles_filename, make_textclip=make_subtitle_clip)

    # Set the duration of the subtitles clip to the duration of the video
    subtitles = subtitles.set_duration(video.duration)

    # Composite video clip with subtitles
    final_video = CompositeVideoClip([video, subtitles.set_position(('center', 'center'))])
    final_video.write_videofile("final_video_with_subtitles.mp4", codec="libx264", fps=30)  # Ensure output is also 30fps

    return "final_video_with_subtitles.mp4"
