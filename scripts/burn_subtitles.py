from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

def burn_subtitles(video_filename, subtitle_filename):
    # Load video clip
    video = VideoFileClip(video_filename)
    # Load subtitles
    subs = pysrt.open(subtitle_filename)

    # Generate subtitle clips
    subtitles = []
    for sub in subs:
        # Create a text clip for each subtitle
        txt_clip = TextClip(sub.text, fontsize=24, color='white', font='Arial-Bold')
        txt_clip = txt_clip.set_position('bottom').set_duration(sub.end.ordinal - sub.start.ordinal) \
                   .set_start(sub.start.ordinal / 1000)  # Convert to seconds
        subtitles.append(txt_clip)

    # Overlay subtitles on the original video
    final = CompositeVideoClip([video] + subtitles)

    # Write the result to a file
    final_video_path = "final_video_with_subtitles.mp4"
    final.write_videofile(final_video_path, codec="libx264", audio_codec='aac')

    return final_video_path
