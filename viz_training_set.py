import numpy as np
import cPickle
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

with open(args.input, 'r') as f:
  data = cPickle.load(f)

patches = data['all_patches']
import random
random.shuffle(patches)

last = 0
for patch, label in patches:
  if label == last: continue
  if patch.size == 0: continue
  print patch, patch.shape
  plt.imshow(patch)
  print label
  plt.show()
  last = label
