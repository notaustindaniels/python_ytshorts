import openai
import json

def select_segments(script_path, srt_path, api_key):
    openai.api_key = api_key
    
    # Read the script content from the file
    with open(script_path, 'r', encoding='utf-8') as file:
        script_content = file.read()
    
    # Read the .srt file content
    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    # Constructing the prompt
    prompt = f"""
Script:
{script_content}

Timestamps:
{srt_content}
"""

    # Making the API call to ChatGPT model
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """
Read the script and the provided timestamps. Output a JSON list of segments of the script where each segment is determined by its potential to be represented by a single artistic image. For each segment, include the script segment, the start time, and the end time. The JSON output should be formatted as follows:

[{{'text': 'script_portion/script_segment', 'start': 'start_time', 'end': 'end_time'}}, ...]

YOU ONLY RESPOND WITH JSON.
"""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    
    # Attempt to parse the JSON response from ChatGPT
    try:
        # Correctly accessing the response data
        segments = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("Failed to decode JSON. Check the model's response.")
        segments = []

    return segments
