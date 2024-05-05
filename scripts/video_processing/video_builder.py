from moviepy.editor import concatenate_videoclips, AudioFileClip, CompositeVideoClip, ImageClip
from moviepy.video.compositing.transitions import slide_in, slide_out
from .parse_time import parse_time  # Import the parse_time function
import os

EFFECT_DURATION = 0.5  # Duration of the slide transition effect

def build_video(clips, voiceover_filename, durations, output_file="final_video.mp4"):
    if not os.path.isfile(voiceover_filename):
        print(f"Audio file not found: {voiceover_filename}")
        return None

    audio_clip = AudioFileClip(voiceover_filename)
    print(f"Loaded audio file with duration: {audio_clip.duration} seconds")

    if not clips:
        print("No video clips were created.")
        return None

    # Resize all clips to the same size as the first clip
    base_size = clips[0].size
    resized_clips = [clip.resize(base_size) for clip in clips]

    # Create transitions for each clip
    video_clips = []
    for i, clip in enumerate(resized_clips):
        start_time = parse_time(durations[i]['start'])  # Use parse_time to convert start time
        end_time = parse_time(durations[i]['end'])  # Use parse_time to convert end time
        clip_duration = end_time - start_time

        if i == 0:  # First clip
            video_clip = CompositeVideoClip(
                [clip.set_start(start_time).set_duration(clip_duration).fx(slide_out, duration=EFFECT_DURATION, side="left")]
            )
        elif i == len(resized_clips) - 1:  # Last clip
            video_clip = CompositeVideoClip(
                [clip.set_start(start_time).set_duration(clip_duration).fx(slide_in, duration=EFFECT_DURATION, side="right")]
            )
        else:  # Middle clips
            video_clip = CompositeVideoClip(
                [clip.set_start(start_time).set_duration(clip_duration).fx(slide_in, duration=EFFECT_DURATION, side="right")]
            ).fx(slide_out, duration=EFFECT_DURATION, side="left")

        video_clips.append(video_clip)

    final_clip = CompositeVideoClip(video_clips).set_audio(audio_clip)
    final_clip.write_videofile(output_file, fps=30, threads=2)
    print(f"Video creation complete, file saved to: {output_file}")
    return output_file
