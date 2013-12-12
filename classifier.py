from generate_textons import generate_textons
from feature_extraction import FeatureExtractor
from visualize_patches import visualize_patches
from sklearn import svm, cross_validation, grid_search

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

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(feature_vectors, labels, test_size=.2, random_state=0)

        # train the classifier on the training data
        svc = svm.SVC()
        params = {'kernel':('linear',), 'C':[1e-3]}
        self.classifier = grid_search.GridSearchCV(svc, params)
        self.classifier.fit(X_train, y_train)
        print 'Best params:', self.classifier.best_params_

        print 'Training data size:', len(X_train)
        print 'Result on test set:', self.classifier.score(X_test, y_test)

    def predict(self,patch):
        """Predict the label of a patch using the trained classifier"""

        return self.classifier.predict(self.fe.get_feature_vector(patch))
