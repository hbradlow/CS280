import numpy as np
import scipy.ndimage
from PIL import Image
import config

def normalize_patches(patches):
    """Normalizes a patch - subracts mean and divides by l1 norm."""
    out = patches - patches.mean(axis=1)[:,None]
    out /= abs(patches).sum(axis=1)[:,None] + .001
    return out

def canonicalize_image(image):
  zoom_factor = config.WINDOW_SIZE / float(max(image.shape[:2]))
  return scipy.ndimage.interpolation.zoom(image, (zoom_factor, zoom_factor, 1))

def rect_to_patch(p):
  im = Image.fromarray(p)
  im.thumbnail((config.PATCH_SIZE, config.PATCH_SIZE))
  return np.array(im)
