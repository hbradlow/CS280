import scipy.ndimage
import config

def normalize_patches(patches):
    """Normalizes a patch - subracts mean and divides by l1 norm."""
    out = patches - patches.mean(axis=1)[:,None]
    out /= abs(patches).sum(axis=1)[:,None] + .001
    return out


def canonicalize_image(image):
  zoom_factor = config.WINDOW_SIZE / float(max(image.shape[:2]))
  return scipy.ndimage.interpolation.zoom(image, (zoom_factor, zoom_factor, 1))
