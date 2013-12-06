import cv2
import cv
import IPython
import time
import cPickle
import config

import numpy as np
from sklearn.feature_extraction import image as skimage
from sklearn.cluster import KMeans


def generate_textons(args):
    W = 640
    H = 480
    IMAGE_SIZE = (W,H)
    margin = .2

    capture = cv2.VideoCapture(args.input_video)

    textons = []

    old_image = None
    counter = 0

    for i in range(1):
        retval,image = capture.read()
        image = cv2.cvtColor(image,cv2.cv.CV_RGB2GRAY)
        image = cv2.resize(image,IMAGE_SIZE).astype(float)/255.
        image = image[W*margin:W*(1-margin),H*margin:H*(1-margin)]
        patches = skimage.extract_patches_2d(image, (config.TEXTON_SIZE,config.TEXTON_SIZE))
        patches = patches.reshape((-1,config.TEXTON_SIZE*config.TEXTON_SIZE))

        #normalize
        patches -= np.mean(patches,axis=1)[:,None]
        patches /= abs(patches).sum(axis=1)[:,None]+.001

        textons.append(patches)

        print counter
        counter += 1

    textons = np.vstack(textons)
    print textons.shape
    km = KMeans(25,verbose=1,max_iter=20,n_init=1)
    print "Clustering..."
    km.fit(textons)
    centers = km.cluster_centers_

    if args.viz:
      import matplotlib.pyplot as plt
      preview = centers.reshape((centers.shape[0],config.TEXTON_SIZE,config.TEXTON_SIZE))
      for t in preview:
        x = t - t.min()
        x /= x.max()
        print x, x.shape
        plt.imshow(x, 'Greys_r')
        plt.show()

    with open(args.output, 'w') as f:
      cPickle.dump(centers, f)

    return centers
