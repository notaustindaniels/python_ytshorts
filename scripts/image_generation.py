from openai import OpenAI

def generate_images(script, api_key):
    client = OpenAI(api_key=api_key)
    sentences = script.split('.')
    images = []

    for idx, sentence in enumerate(sentences):
        response = client.images.generate(
            model="dall-e-3",
            prompt=sentence,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        image_url = response.data[0].url
        images.append(image_url)

    return images
