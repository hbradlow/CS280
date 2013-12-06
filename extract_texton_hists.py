import numpy as np
import sklearn
import sklearn.feature_extraction
import scipy.spatial.distance as ssd
import config

PATCH_SIZE = 50

# texton dictionary format: N x K array
# where N is the dictionary size, K is the texton dimensionality
texton_dict = np.empty((N, K))

def normalize_patches(patches):
  out = patches - patches.mean(axis=1)[:,None]
  out /= abs(patches).sum(axis=1)[:,None] + .001
  return out

def compute_texton_hist(textons, patch):
  assert textons.shape[1] == config.TEXTON_SIZE**2

  subpatches = sklearn.feature_extraction.image.extract_patches_2d(patch, (config.TEXTON_SIZE, config.TEXTON_SIZE)).resize((-1, config.TEXTON_SIZE**2))
  subpatches = normalize_patches(subpatches)

  dists = ssd.cdist(subpatches, textons, 'euclidean')
  best_textons = dists.amin(axis=1)

  assert len(best_textons) == patches.shape[0]

# hist = np.zeros(len(textons))
# for i in range(len(patches)):
#   hist[best_textons[i]] += 1.
# hist /= hist.sum()

  hist = np.bincount(best_textons, minlength=len(textons))
  hist /= hist.sum()

  return hist


