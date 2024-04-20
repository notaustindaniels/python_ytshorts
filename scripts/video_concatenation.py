from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
import json

def concatenate_video(images, durations_file, voiceover_filename):
    # Load durations from JSON file
    with open(durations_file, 'r') as f:
        durations = json.load(f)

    clips = []
    # Load the voiceover as the base audio clip
    audio_clip = AudioFileClip(voiceover_filename)
    
    # Process each image and its duration
    for item in durations:
        image_path = next((img['image_path'] for img in images if img['image_id'] == item['image_id']), None)
        if image_path:
            # Create an image clip with the specified duration
            image_clip = ImageClip(image_path).set_duration(item['end'] - item['start']).set_start(item['start']).set_audio(audio_clip.subclip(item['start'], item['end']))
            clips.append(image_clip)

    # Combine all clips into a single video
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip = final_clip.set_audio(audio_clip)
    final_video_path = "final_video.mp4"
    final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac')
    
    return final_video_path
