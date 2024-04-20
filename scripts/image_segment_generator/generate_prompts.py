def generate_prompts(segments):
    prompts = [{'image_id': idx, 'prompt': f"Generate an image representing this scene: {seg['text']}"} for idx, seg in enumerate(segments)]
    return prompts
