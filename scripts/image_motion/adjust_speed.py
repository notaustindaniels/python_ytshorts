def adjust_speed(clip, duration):
    return clip.fx(vfx.speedx, lambda t: 1 if t < 0.67 * duration else 0.5)
