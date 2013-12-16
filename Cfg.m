classdef Cfg
  properties (Constant = true)
    % Pipeline intermediate files
    LABEL_FILE = 'out/training/labels.mat';
    POS_EXAMPLES_DIR = 'out/training/pos';
    NEG_EXAMPLES_DIR = 'out/training/neg';
    CLASSIFIER_FILE = 'out/training/classifier.mat';
    TRAINING_SET_FRAC = .75;
    
    % Algorithm parameters
    PATCH_SIZE = 40;
    NUM_HIST_BINS = 10;
    
  end
end
