from moviepy.editor import vfx

def pan_image(clip, duration):
    return clip.fx(vfx.scroll, w=clip.w, h=0, x_speed=clip.w / duration)
