import json

def assign_durations(segments):
    durations = [{'image_id': idx, 'start': seg['start'], 'end': seg['end']} for idx, seg in enumerate(segments)]
    with open('durations.json', 'w') as f:
        json.dump(durations, f)
    return durations
