import json

def assign_durations(segments):
    """
    This function takes a list of segments each containing 'start' and 'end' times.
    It assigns these times directly to the corresponding images.
    
    Args:
    segments (list): A list of dictionaries where each dictionary has an 'image_id', 'text',
                     'start', and 'end' key, which comes from the select_segments output.
    
    Returns:
    list: Returns a list of dictionaries with assigned start and end durations for images.
    """
    durations = []
    for idx, seg in enumerate(segments):
        try:
            # Using the same data structure as in the provided segments
            durations.append({
                'image_id': idx,
                'start': seg['start'],  # Assuming start time is correctly formatted
                'end': seg['end']       # Assuming end time is correctly formatted
            })
        except KeyError as e:
            print(f"Missing data in segment: {str(e)}")

    # Optional: Save durations to a file
    with open('durations.json', 'w') as f:
        json.dump(durations, f, ensure_ascii=False, indent=4)
    
    return durations