import openai

def generate_images(sentences, api_key):
    openai.api_key = api_key
    images = []
    for sentence in sentences:
        response = openai.Image.create(
            prompt=sentence,
            n=1,
            size="1024x1024",
            model="dall-e-2"
        )
        images.append(response['data'][0]['url'])  # Assuming URL handling for simplicity
    return images
