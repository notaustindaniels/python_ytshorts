import openai

def generate_prompts(segments, api_key):
    client = openai.OpenAI(api_key=api_key)
    prompts = []
    for idx, seg in enumerate(segments):
        try:
            # Call to ChatGPT-3.5 Turbo to refine or create the image generation prompt
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative writer. Generate a compelling and detailed image description in just one sentence, or less. Your responses are ALWAYS one sentence or less."},
                    {"role": "user", "content": f'''Create a detailed description for an image that represents: {seg['text']}
                     
                     in two sentences or less.'''}
                ],
                max_tokens=150
            )
            # Extract the generated prompt from the response
            generated_prompt = response.choices[0].message.content
            prompts.append({
                'image_id': idx,
                'prompt': generated_prompt,
                'start': seg['start'],
                'end': seg['end']
            })
        except openai.APIError as e:
            print(f"API error for segment '{seg['text']}': {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    return prompts
