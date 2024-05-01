import json
from .parse_time import parse_time
from .clip_manager import create_image_clips
from .video_builder import build_video


def concatenate_video(images, durations_file, voiceover_filename):
    print(f"Loading durations file: {durations_file}")
    with open(durations_file, 'r') as f:
        durations = json.load(f)

    clips = create_image_clips(images, durations)
    final_video_path = build_video(clips, voiceover_filename)
    return final_video_path
