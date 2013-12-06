import cv2
import cv
import IPython
import time

import numpy as np
from sklearn.feature_extraction import image as skimage
from sklearn.cluster import KMeans

PATCH_SIZE = 5
W = 640
H = 480
IMAGE_SIZE = (W,H)
margin = .2

capture = cv2.VideoCapture("/Users/jonathan/Desktop/textons.MOV")

textons = []

old_image = None
counter = 0

for i in range(1):
    retval,image = capture.read()
    image = cv2.cvtColor(image,cv2.cv.CV_RGB2GRAY)
    IPython.embed()
    image = cv2.resize(image,IMAGE_SIZE).astype(float)/255.
    image = image[W*margin:W*(1-margin),H*margin:H*(1-margin)]
    patches = skimage.extract_patches_2d(image, (PATCH_SIZE,PATCH_SIZE))
    patches = patches.reshape((-1,PATCH_SIZE*PATCH_SIZE))

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
IPython.embed()
preview = centers.reshape((centers.shape[0],PATCH_SIZE,PATCH_SIZE))
cv2.namedWindow("test")
IPython.embed()
