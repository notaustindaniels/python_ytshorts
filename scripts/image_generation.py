from openai import OpenAI

def generate_images(script, api_key):
    client = OpenAI(api_key=api_key)
    # Ensure that script is not None and strip whitespace
    sentences = [sentence.strip() for sentence in script.split('.') if sentence.strip()]
    images = []

    for idx, sentence in enumerate(sentences):
        if sentence:  # Check if the sentence is not empty
            response = client.images.generate(
                model="dall-e-3",
                prompt=sentence,
                n=1,
                size="1024x1792",
                quality="standard"
            )
            image_url = response.data[0].url
            images.append(image_url)

    return images
