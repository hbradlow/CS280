import numpy as np
import scipy.misc

def visualize_patches(patches):
    grid = np.hstack(patches)
    scipy.misc.imsave("output.jpg",grid)
