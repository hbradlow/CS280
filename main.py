import argparse
import cv2
import cPickle
from classifier import Classifier
import sklearn.feature_extraction.image
import config
import numpy as np
import scipy.misc

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('training_data')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

with open(args.training_data, 'r') as f:
  training_data = cPickle.load(f)

classifier = Classifier(args.input_video, training_data['all_patches'], debug=True)

capture = cv2.VideoCapture(args.input_video)

for i in range(1):
    retval,image = capture.read()

    image_save = np.array(cv2.resize(image,(640,480)).astype(float))
    image = cv2.resize(image,(640,480)).astype(float)/255.
    image = np.array(image)
    h,w = image.shape[0:2]
    
    for i in range(h-config.PATCH_SIZE):
        if i%10 == 0:
            print i
            for j in range(w-config.PATCH_SIZE):
                patch = image[i:i+config.PATCH_SIZE,j:j+config.PATCH_SIZE,:]
                print patch.shape
                if 1 in classifier.predict(patch):
                    image_save[i,j,:] = [255,0,0]

    scipy.misc.imsave("output.jpg",image_save)

    exit()
