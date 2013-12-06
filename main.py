import argparse
from generate_textons import generate_textons
from feature_extraction import FeatureExtractor
from sklearn import svm

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

textons = generate_textons(args)
fe = FeatureExtractor(textons)

feature_vectors = []
labels = []

for patch,label in get_patches(args.input_video):
    feature_vector = get_feature_vector(textons,patch)
    labels.append(label)
    feature_vectors.append(feature_vector)

classifier = svm.SVC()
classifier.fit(feature_vectors,labels)
