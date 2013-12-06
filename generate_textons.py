import cv2
import cPickle
import config
import numpy as np
from sklearn.feature_extraction import image as skimage
from sklearn.cluster import KMeans

from utils import normalize_patches

def generate_textons(input_video, W=640, H=480, margin=.2, viz=False, output=None, debug=False):
    """Generate a texton dictionary for a given input video."""
    IMAGE_SIZE = (W,H)

    capture = cv2.VideoCapture(input_video)

    textons = []

    counter = 0

    for i in range(1):
        # grab a frame from the video and reformat it (gray,normalize values, trim)
        retval,image = capture.read()
        image = cv2.cvtColor(image,cv2.cv.CV_RGB2GRAY)
        image = cv2.resize(image,IMAGE_SIZE).astype(float)/255.
        image = image[W*margin:W*(1-margin),H*margin:H*(1-margin)]

        # extract patches from the frame and vectorize and normalize
        patches = skimage.extract_patches_2d(image, 
                                    (config.TEXTON_SIZE,config.TEXTON_SIZE))
        patches = patches.reshape((-1,config.TEXTON_SIZE*config.TEXTON_SIZE))
        patches = normalize_patches(patches)

        textons.append(patches)

        if debug:
            print counter
        counter += 1

    textons = np.vstack(textons)

    # cluster the textons and extract the centers of the clusters
    print "Clustering..."
    km = KMeans(25,verbose=1,max_iter=20,n_init=1)
    km.fit(textons)
    centers = km.cluster_centers_

    # display the clusters
    if viz:
      import matplotlib.pyplot as plt
      preview = centers.reshape((centers.shape[0],
                            config.TEXTON_SIZE,config.TEXTON_SIZE))
      for t in preview:
        x = t - t.min()
        x /= x.max()
        print x, x.shape
        plt.imshow(x, 'Greys_r')
        plt.show()

    # output the clusters to a file
    if output:
        with open(output, 'w') as f:
          cPickle.dump(centers, f)

    return centers
