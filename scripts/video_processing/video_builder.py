from moviepy.editor import concatenate_videoclips, AudioFileClip, CompositeVideoClip, ColorClip
from moviepy.video.compositing.transitions import slide_in, slide_out
from .parse_time import parse_time
import os

EFFECT_DURATION = 0.5  # Duration of the slide transition effect
DISPLAY_WIDTH = 1792
DISPLAY_HEIGHT = 1024
LENS_WIDTH = 576
LENS_HEIGHT = 1024  # Maintained height to match display height for 9:16 aspect ratio

def build_video(clips, voiceover_filename, durations, output_file="final_video.mp4"):
    if not os.path.isfile(voiceover_filename):
        print(f"Audio file not found: {voiceover_filename}")
        return None

    audio_clip = AudioFileClip(voiceover_filename)
    print(f"Loaded audio file with duration: {audio_clip.duration} seconds")

    if not clips:
        print("No video clips were created.")
        return None

    # Create a base clip with the original display size
    base_clip = ColorClip(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_clip.duration)

    # Create black borders
    left_border = ColorClip(size=((DISPLAY_WIDTH - LENS_WIDTH) // 2, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_clip.duration)
    right_border = ColorClip(size=((DISPLAY_WIDTH - LENS_WIDTH) // 2, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_clip.duration)

    # Create transitions and scrolling effect for each clip
    video_clips = []
    for i, clip in enumerate(clips):
        end_time = parse_time(durations[i]['end'])
        start_time = parse_time(durations[i]['start']) if i > 0 else 0
        clip_duration = end_time - start_time
        video_clip = clip.set_position("center").set_start(start_time).set_duration(clip_duration)

        if i < len(clips) - 1:
            next_clip = clips[i + 1]
            transition_start_time = end_time - EFFECT_DURATION
            video_clip = CompositeVideoClip([
                video_clip,
                video_clip.fx(slide_out, duration=EFFECT_DURATION, side="left"),
                next_clip.set_position("center").set_start(transition_start_time).set_duration(EFFECT_DURATION + (parse_time(durations[i + 1]['start']) - end_time)).fx(slide_in, duration=EFFECT_DURATION, side="right")
            ])
        video_clips.append(video_clip)

    # Composite the video clips and black borders onto the base clip
    final_clip = CompositeVideoClip([
        base_clip,
        CompositeVideoClip(video_clips).set_position("center"),
        left_border.set_position(("left", "center")),
        right_border.set_position(("right", "center"))
    ]).set_audio(audio_clip)

    final_clip.write_videofile(output_file, fps=30, threads=2)
    print(f"Video creation complete, file saved to: {output_file}")
    return output_file
