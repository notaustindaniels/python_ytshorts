import re
import json

def parse_srt_time(time_str):
    """Convert SRT time format 'HH:MM:SS,ms' to total seconds."""
    match = re.match(r'(\d+):(\d+):(\d+),(\d+)', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")
    hours, minutes, seconds, milliseconds = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0

def assign_durations(segments):
    durations = []
    for idx, seg in enumerate(segments):
        try:
            start_seconds = parse_srt_time(seg['start'])
            end_seconds = parse_srt_time(seg['end'])
            durations.append({
                'image_id': idx,
                'start': start_seconds,
                'end': end_seconds
            })
        except ValueError as e:
            print(f"Error parsing time: {e}")
    with open('durations.json', 'w') as f:
        json.dump(durations, f, ensure_ascii=False, indent=4)
    return durations
