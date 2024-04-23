from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

def burn_subtitles(video_filename, subtitle_filename):
    video = VideoFileClip(video_filename)
    subs = pysrt.open(subtitle_filename)

    subtitles = [TextClip(sub.text, fontsize=100, color='yellow', font='/Users/austin/python_ytshorts/fonts/bold_font.ttf', stroke_color="black", stroke_width=5)
                 .set_position('center', 'center')
                 .set_duration((sub.end.ordinal - sub.start.ordinal) / 1000)  # Convert milliseconds to seconds
                 .set_start(sub.start.ordinal / 1000)  # Start time also in seconds
                 for sub in subs]

    final = CompositeVideoClip([video] + subtitles)
    final_video_path = "final_video_with_subtitles.mp4"
    final.write_videofile(final_video_path, threads=2)

    return final_video_path