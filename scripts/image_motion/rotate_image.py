from moviepy.editor import vfx

def rotate_image(clip, duration):
    return clip.fx(vfx.rotate, 180 * (clip.time / duration) - 90)
