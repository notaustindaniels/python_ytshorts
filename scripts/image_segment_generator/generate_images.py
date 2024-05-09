import openai
import requests  # Needed to download images
import os  # Needed for handling directories

def generate_images(prompts, api_key):
    client = openai.OpenAI(api_key=api_key)
    images = []
    for prompt in prompts:
        try:
            # Generate the image
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt['prompt'],
                n=1,
                size="1792x1024"
            )
            # Assuming response.data[0] reliably contains the image URL
            image_url = response.data[0].url
            image_path = f"images/image_{prompt['image_id']}.png"
            
            # Check if the directory exists, if not create it
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                images.append({
                    'image_id': prompt['image_id'],
                    'image_path': image_path,
                    'start': prompt['start'],
                    'end': prompt['end']
                })
                print(f"Saved image to {image_path}")
            else:
                print(f"Failed to download image from {image_url}")

        except openai.APIError as e:
            print(f"API error for prompt '{prompt['prompt']}': {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    return images
