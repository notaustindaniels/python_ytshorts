import random
from .rotate_image import rotate_image
from .zoom_image import zoom_image
from .pan_image import pan_image
from .adjust_speed import adjust_speed

def apply_random_motion(clip, duration):
    motion_effects = [
        lambda c: rotate_image(c, duration),
        lambda c: zoom_image(c, duration),
        lambda c: pan_image(c, duration),
        lambda c: adjust_speed(c, duration)
    ]
    
    selected_effects = random.sample(motion_effects, random.randint(1, len(motion_effects)))
    
    for effect in selected_effects:
        clip = effect(clip)
    
    return clip
