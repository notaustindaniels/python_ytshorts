from openai import OpenAI

def generate_images(prompts, api_key):
    client = OpenAI(api_key=api_key)
    images = []
    for prompt in prompts:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt['description'],
            n=1,
            size="1024x1792",
            quality="standard"
        )
        image_url = response.data[0].url
        start_time = prompt['start']
        end_time = prompt['end']
        images.append({
            'image_url': image_url,
            'start': start_time,
            'end': end_time
        })
    return images
