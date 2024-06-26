from moviepy.editor import *
import os
import json

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
    max_duration = 0

    for item in durations:
        image_path = next((img['image_path'] for img in images if img['image_id'] == item['image_id']), None)
        if image_path and os.path.isfile(image_path):
            start_time = item['start']
            end_time = item['end']
            clip_duration = end_time - start_time
            image_clip = ImageClip(image_path).set_duration(clip_duration).set_start(start_time)
            clips.append(image_clip)
            max_duration = max(max_duration, end_time)

    if not clips:
        print("No video clips were created.")
        return None

    video_clip = concatenate_videoclips(clips, method="compose").set_duration(max_duration)
    
    # Adjust the audio clip's duration to match the video's duration
    if audio_clip.duration > max_duration:
        audio_clip = audio_clip.subclip(0, max_duration)

    final_clip = video_clip.set_audio(audio_clip)
    final_video_path = "final_video.mp4"
    final_clip.write_videofile(final_video_path, fps=30, threads=2)
    print("Video creation complete, file saved to:", final_video_path)
    
    return final_video_path
