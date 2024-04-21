from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
import json

def concatenate_video(images, durations_file, voiceover_filename):
    with open(durations_file, 'r') as f:
        durations = json.load(f)

    clips = []
    audio_clip = AudioFileClip(voiceover_filename)
    
    # Process each image and its duration
    for item in durations:
        image_path = next((img['image_path'] for img in images if img['image_id'] == item['image_id']), None)
        if image_path:
            image_clip = ImageClip(image_path).set_duration(item['end'] - item['start']).set_start(item['start']).set_audio(audio_clip.subclip(item['start'], item['end']))
            clips.append(image_clip)
        else:
            print(f"No image path found for image ID {item['image_id']}")

    if not clips:
        print("No video clips were created. Check earlier steps.")
        return None

    # Combine all clips into a single video
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.fps = 24  # Set the frames per second to 24

    # Set audio and write the file
    final_clip = final_clip.set_audio(audio_clip)
    final_video_path = "final_video.mp4"
    final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', fps=24)
    
    return final_video_path
