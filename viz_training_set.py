import numpy as np
import cPickle
import matplotlib.pyplot as plt

with open('out.pkl', 'r') as f:
  data = cPickle.load(f)

patches = data['all_patches']
import random
random.shuffle(patches)

last = 0
for patch, label in patches:
  if label == last: continue
  print patch
  plt.imshow(patch)
  print label
  plt.show()
  last = label
