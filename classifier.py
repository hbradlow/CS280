from generate_textons import generate_textons
from feature_extraction import FeatureExtractor
from sklearn import svm

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
        for patch,label in training_data_patches:
            feature_vector = self.fe.get_feature_vector(patch)
            labels.append(label)
            feature_vectors.append(feature_vector)

        # train the classifier on the training data
        self.classifier = svm.SVC()
        self.classifier.fit(feature_vectors,labels)

    def predict(self,patch):
        """Predict the label of a patch using the trained classifier"""

        return self.classifier.predict(patch)
