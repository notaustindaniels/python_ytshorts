import openai
import json

def log_raw_response(raw_response):
    with open("model_raw_output.txt", "w", encoding='utf-8') as file:
        file.write(raw_response)
    print("Raw model response has been logged to 'model_raw_output.txt'")

def select_segments(script_path, srt_path, api_key):
    openai.api_key = api_key

    with open(script_path, 'r', encoding='utf-8') as file:
        script_content = file.read()

    with open(srt_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    prompt = f"""
    Script:
    {script_content}

    Timestamps:
    {srt_content}
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system", "content": """
Read the script and the provided timestamps. Output a JSON list of segments of the script where each segment is determined by its potential to be represented by a single artistic image. For each segment, include the script segment, the start time, and the end time. The JSON output should be formatted as follows:

[{{'text': 'script_portion/script_segment', 'start': 'start_time', 'end': 'end_time'}}, ...]

YOU ONLY RESPOND WITH JSON.
"""}, {
                "role": "user", "content": prompt
            }],
            max_tokens=1500)
        
        # Log the raw response immediately after receiving it
        log_raw_response(response.choices[0].message.content)

        segments = json.loads(response.choices[0].message.content)
        return segments  # No need to return None for error since there's no error handling needed
    except Exception as e:
        # Log exception details
        log_raw_response(str(e))
        return None  # Indicate a failure without specific error message
