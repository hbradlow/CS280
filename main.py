import argparse
import cv2
import cPickle
from classifier import Classifier
import sklearn.feature_extraction.image
import config
import numpy as np
import scipy.misc
import utils
import IPython

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('training_data')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

with open(args.training_data, 'r') as f:
  input_str = f.read()
training_data = cPickle.loads(input_str)

classifier = Classifier(args.input_video, training_data['all_patches'], debug=True)
IPython.embed()

capture = cv2.VideoCapture(args.input_video)

for i in range(10):
    retval,image = capture.read()

    image = utils.canonicalize_image(image)
    image_save = image.copy()
    # image_save = np.array(cv2.resize(image,(640,480)).astype(float))
    # image = cv2.resize(image,(640,480)).astype(float)/255.
    # image = np.array(image)
    h,w = image.shape[0:2]
    
    for i in range(0,h-config.PATCH_SIZE,5):
        print i
        for j in range(0,w-config.PATCH_SIZE,5):
            patch = image[i:i+config.PATCH_SIZE,j:j+config.PATCH_SIZE,:]
            if 1 in classifier.predict(patch):
                for i2 in range(i,i+10):
                    for j2 in range(j,j+10):
                        image_save[i2,j2,:] = [255,0,0]

    scipy.misc.imsave("output.jpg",image_save)

    raw_input()
