from extract_texton_hists import compute_texton_hist
import numpy as np

class FeatureExtractor:
    def __init__(self,textons,bins=3):
        self.textons = textons
        self.bins = 50
    def get_feature_vector(self,patch):
        gray_patch = np.mean(patch,axis=2)
        linear_patch = patch.reshape((-1,3))

        texton_hist = compute_texton_hist(self.textons,gray_patch)
        color_hist = np.histogramdd(linear_patch,bins=self.bins,range=((-.5,255.5),(-.5,255.5),(-.5,255.5)))[0].reshape(-1)

        return np.r_[texton_hist, color_hist]
