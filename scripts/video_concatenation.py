from moviepy.editor import *
import os
import json

def parse_time(time_str):
    """
    Parses time in format HH:MM:SS or HH:MM:SS,ms and returns total seconds as a float.
    Handles time strings with and without milliseconds.
    """
    parts = time_str.split(':')
    hours, minutes = int(parts[0]), int(parts[1])
    seconds_parts = parts[2].split(',')  # Split seconds and milliseconds if milliseconds are present
    seconds = float(seconds_parts[0])  # Convert seconds to float

    if len(seconds_parts) > 1:
        milliseconds = int(seconds_parts[1])
        total_seconds = 3600 * hours + 60 * minutes + seconds + milliseconds / 1000.0
    else:
        total_seconds = 3600 * hours + 60 * minutes + seconds

    return total_seconds

def concatenate_video(images, durations_file, voiceover_filename):
    print(f"Loading durations file: {durations_file}")
    with open(durations_file, 'r') as f:
        durations = json.load(f)

    if not os.path.isfile(voiceover_filename):
        print(f"Audio file not found: {voiceover_filename}")
        return None

    audio_clip = AudioFileClip(voiceover_filename)
    print(f"Loaded audio file with duration: {audio_clip.duration} seconds")

    clips = []
    current_start_time = 0.0  # This will keep track of when the last clip ended

    for item in durations:
        image_path = next((img['image_path'] for img in images if img['image_id'] == item['image_id']), None)
        if image_path and os.path.isfile(image_path):
            try:
                end_time = parse_time(item['end'])
                if not clips:  # If it's the first clip
                    start_time = parse_time(item['start'])  # Use the start time from the file for the first clip
                else:
                    start_time = current_start_time  # Subsequent clips start right after the previous one ends

                clip_duration = end_time - start_time
                image_clip = ImageClip(image_path).set_duration(clip_duration).set_start(start_time)
                clips.append(image_clip)
                current_start_time = end_time  # Update the start time for the next clip
            except Exception as e:
                print(f"Error processing time data for {item['image_id']}: {e}")

    if not clips:
        print("No video clips were created.")
        return None

    video_clip = concatenate_videoclips(clips, method="compose")

    # Ensure the final clip extends to the end of the audio if necessary
    final_end_time = max(current_start_time, audio_clip.duration)
    last_clip = clips[-1]
    extended_duration = final_end_time - last_clip.start
    extended_last_clip = last_clip.set_duration(extended_duration)
    clips[-1] = extended_last_clip  # Replace the last clip with the extended version

    video_clip = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)
    final_video_path = "final_video.mp4"
    video_clip.write_videofile(final_video_path, fps=30, threads=2)
    print(f"Video creation complete, file saved to: {final_video_path}")

    return final_video_path