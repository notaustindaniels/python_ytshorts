from .parse_time import parse_time
from moviepy.editor import ImageClip
import os

def create_image_clips(images, durations):
    clips = []
    current_start_time = 0.0  # Ensure we start from zero or from a predefined start time if needed

    for item in durations:
        image_path = next((img['image_path'] for img in images if img['image_id'] == item['image_id']), None)
        if image_path and os.path.isfile(image_path):
            start_time = parse_time(item['start'])
            end_time = parse_time(item['end'])

            if not clips:
                current_start_time = start_time  # Start time for first clip
            else:
                # Adjust so the next clip starts exactly when the previous ends
                current_start_time = clips[-1].end

            clip_duration = end_time - current_start_time
            if clip_duration < 0:
                print(f"Error: Negative duration calculated for clip starting at {current_start_time} and ending at {end_time}")
                continue

            image_clip = ImageClip(image_path).set_duration(clip_duration).set_start(current_start_time)
            clips.append(image_clip)

    return clips