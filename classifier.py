from generate_textons import generate_textons
from feature_extraction import FeatureExtractor
from visualize_patches import visualize_patches
from sklearn import svm
import IPython

class Classifier:

    def __init__(self,input_video,training_data_patches,debug=False):
        """Train the classifier on the training data using a texton dictionary"""

        self.debug=debug

        # generate the texton dictionary
        self.textons = generate_textons(input_video,debug=self.debug)

        # extract the feature vectors from the training video
        self.fe = FeatureExtractor(self.textons)
        feature_vectors = []
        labels = []
        patches = []
        for patch,label in training_data_patches:
            patches.append(patch)
            feature_vector = self.fe.get_feature_vector(patch)
            labels.append(label)
            feature_vectors.append(feature_vector)
        visualize_patches(patches[0:30])

        # train the classifier on the training data
        self.classifier = svm.SVC()
        self.classifier.fit(feature_vectors,labels)

    def predict(self,patch):
        """Predict the label of a patch using the trained classifier"""

        print self.classifier.predict(self.fe.get_feature_vector(patch))
        return self.classifier.predict(self.fe.get_feature_vector(patch))
