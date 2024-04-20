def generate_prompts(segments):
    prompts = []
    for idx, seg in enumerate(segments):
        prompts.append({
            'image_id': idx,
            'prompt': f"Generate an image representing this scene: {seg['text']}",
            'start': seg['start'],   # Include start time
            'end': seg['end']        # Include end time
        })
    return prompts
