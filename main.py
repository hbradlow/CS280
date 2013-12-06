import argparse
from classifier import Classifier

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

classifier = Classifier(args.input_video,debug=True)
