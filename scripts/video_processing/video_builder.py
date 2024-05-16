from moviepy.editor import concatenate_videoclips, AudioFileClip, CompositeVideoClip, ColorClip
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
    audio_duration = audio_clip.duration
    print(f"Loaded audio file with duration: {audio_duration} seconds")

    if not clips:
        print("No video clips were created.")
        return None

    # Create a base clip with the original display size
    base_clip = ColorClip(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_duration)

    # Create black borders
    left_border_width = (DISPLAY_WIDTH - LENS_WIDTH) // 2
    right_border_width = (DISPLAY_WIDTH - LENS_WIDTH) // 2

    left_border = ColorClip(size=(left_border_width, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_duration)
    right_border = ColorClip(size=(right_border_width, DISPLAY_HEIGHT), color=(0, 0, 0), duration=audio_duration)

    # Custom slide-in and slide-out functions
    def custom_slide_in(t, start_pos, end_pos):
        return (start_pos + (end_pos - start_pos) * (t / EFFECT_DURATION), "center")

    def custom_slide_out(t, start_pos, end_pos):
        return (start_pos + (end_pos - start_pos) * (t / EFFECT_DURATION), "center")

    video_clips = []
    previous_end_time = 0
    for i, clip in enumerate(clips):
        end_time = parse_time(durations[i]['end'])
        clip_duration = end_time - previous_end_time
        final_pos = left_border_width

        # Ensure the clip lasts until its designated end_time
        base_clip = clip.set_position((final_pos, 'center')).set_start(previous_end_time).set_duration(clip_duration)

        if i < len(clips) - 1:
            next_clip = clips[i + 1]
            transition_start_time = end_time

            # Current clip with slide out effect
            current_clip_with_effect = clip.set_position(lambda t: custom_slide_out(t, final_pos, -DISPLAY_WIDTH)).set_start(end_time).set_duration(EFFECT_DURATION)

            # Next clip with slide in effect
            next_clip_with_effect = next_clip.set_position(lambda t: custom_slide_in(t, DISPLAY_WIDTH, final_pos)).set_start(end_time).set_duration(EFFECT_DURATION)

            video_clips.append(base_clip.set_duration(end_time - previous_end_time))
            video_clips.append(current_clip_with_effect)
            video_clips.append(next_clip_with_effect)
            previous_end_time = end_time + EFFECT_DURATION
        else:
            # Last clip runs until the end of the audio
            final_clip_duration = audio_duration - previous_end_time
            final_clip = clip.set_position((final_pos, "center")).set_start(previous_end_time).set_duration(final_clip_duration)
            video_clips.append(final_clip)

    # Composite the video clips and black borders onto the base clip
    final_clip = CompositeVideoClip([
        *video_clips,
        left_border.set_position(("left", "center")),
        right_border.set_position(("right", "center"))
    ]).set_audio(audio_clip)

    final_clip.write_videofile(output_file, fps=30, threads=2)
    print(f"Video creation complete, file saved to: {output_file}")
    return output_file
