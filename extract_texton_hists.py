import numpy as np
import sklearn
import sklearn.feature_extraction
import scipy.spatial.distance as ssd

import config
from utils import normalize_patches

def compute_texton_hist(textons, patch):
    """Computes a histogram of the occurence of textons within a patch."""

    assert textons.shape[1] == config.TEXTON_SIZE**2

    # extract small patches and normalize
    subpatches = sklearn.feature_extraction.image.extract_patches_2d(patch, (config.TEXTON_SIZE, config.TEXTON_SIZE)).resize((-1, config.TEXTON_SIZE**2))
    subpatches = normalize_patches(subpatches)

    # finds the closest matching texton for each subpatch
    dists = ssd.cdist(subpatches, textons, 'euclidean')
    best_textons = dists.amin(axis=1)

    assert len(best_textons) == patches.shape[0]

    # computes a histogram of the matching textons
    hist = np.bincount(best_textons, minlength=len(textons))
    hist /= hist.sum()

    return hist
