import argparse
import cv2
import cPickle
from classifier import Classifier
import sklearn.feature_extraction.image
import config

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
    patches = sklearn.feature_extraction.image.extract_patches_2d(image, (config.PATCH_SIZE, config.PATCH_SIZE))
    print patches.shape

    for patch in patches:
        if 1 in classifier.predict(patch):
            print "Found one"
