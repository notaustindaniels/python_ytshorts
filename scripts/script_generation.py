import openai

def generate_script(video_idea, api_key):
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate a short video script from the first person perspective in a casual/informal/conversational tone.  The script should be no longer than one paragraph.  The script should be based on the following idea: {video_idea}"}
        ]
    )
    return response.choices[0].message.content