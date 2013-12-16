clear; clc; close all;

POS_EXAMPLES_DIR = 'out/training/pos';
NEG_EXAMPLES_DIR = 'out/training/neg';
CLASSIFIER_OUTPUT = 'out/training/classifier.mat';
PATCH_SIZE = 40;

positiveinstances = struct('imageFilename', {}, 'objectBoundingBoxes', {});

% load all examples and compute features
num_pos = 0; num_neg = 0;
for file=dir([POS_EXAMPLES_DIR '/*.png'])'
  i = length(positiveinstances) + 1;
  positiveinstances(i).imageFilename = [POS_EXAMPLES_DIR '/' file.name];
  positiveinstances(i).objectBoundingBoxes = [1 1 40 40];
end

trainCascadeObjectDetector('cascade.xml', positiveinstances, NEG_EXAMPLES_DIR, 'FalseAlarmRate', 0.2, 'NumCascadeStages', 5);
