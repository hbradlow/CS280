import argparse
import cPickle
from classifier import Classifier

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('training_data')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

with open(args.training_data, 'r') as f:
  training_data = cPickle.load(f)

classifier = Classifier(args.input_video, training_data['all_patches'], debug=True)
