import openai

def generate_images(prompts, api_key):
    # Initialize the OpenAI client with your API key
    client = openai.OpenAI(api_key=api_key)
    images = []
    for prompt in prompts:
        try:
            # Call to generate images using the client instance
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt['prompt'],
                n=1,
                size="1024x1792"
            )
            # Assuming the response includes at least one image URL
            image_url = response['data'][0]['url']
            print(f"Generated image URL: {image_url}")  # Debugging output
            images.append({
                'image_id': prompt['image_id'],
                'image_url': image_url,
                'start': prompt['start'],
                'end': prompt['end']
            })
        except openai.APIError as e:  # Handle API-specific errors
            print(f"API error for prompt '{prompt['prompt']}': {str(e)}")
        except Exception as e:  # Handle other potential errors
            print(f"An unexpected error occurred: {str(e)}")

    return images
