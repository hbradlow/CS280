from extract_texton_hists import compute_texton_hist

class FeatureExtractor:
    def __init__(self,textons,bins=3):
        self.textons = textons
        self.bins = 3
    def get_feature_vector(self,patch):
        gray_patch = np.mean(patch,axis=2)
        linear_patch = patch.reshape((-1,3))

        texton_hist = compute_texton_hist(self.textons,gray_patch)
        color_hist = np.histogramdd(linear_patch,bins=self.bins)[0].reshape((-1,1))

        return np.vstack((texton_hist,color_hist))
