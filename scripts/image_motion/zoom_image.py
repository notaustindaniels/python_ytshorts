from moviepy.editor import vfx

def zoom_image(clip, duration):
    return clip.fx(vfx.resize, lambda t: 1 + 0.35 * (t / duration))
