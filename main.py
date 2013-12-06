import argparse
from generate_textons import generate_textons
from feature_extraction import FeatureExtractor
from sklearn import svm

parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output')
parser.add_argument('--viz', default=False)
args = parser.parse_args()

def Classifier:
    def __init__(self):
        self.textons = generate_textons(args,viz=args.viz,output=args.output)
        self.fe = FeatureExtractor(textons)

        feature_vectors = []
        labels = []

        for patch,label in get_patches(args.input_video):
            feature_vector = get_feature_vector(patch)
            labels.append(label)
            feature_vectors.append(feature_vector)

        self.classifier = svm.SVC()
        self.classifier.fit(feature_vectors,labels)
    def predict(self,patch):
        return self.classifier.predict(patch)
