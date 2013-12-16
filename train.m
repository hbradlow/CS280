clear; clc; close all;

POS_EXAMPLES_DIR = 'out/training/pos';
NEG_EXAMPLES_DIR = 'out/training/neg';
CLASSIFIER_OUTPUT = 'out/training/classifier.mat';

% load all examples and compute features
examples = struct('img', {}, 'X', {}, 'y', {});
num_pos = 0; num_neg = 0;
for file=dir([POS_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  examples(i).img = imread([POS_EXAMPLES_DIR '/' file.name]);
  examples(i).y = 1;
end
for file=dir([NEG_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  examples(i).img = imread([NEG_EXAMPLES_DIR '/' file.name]);
  examples(i).y = -1;
end

for i=1:length(examples)
  examples(i).X = compute_features(examples(i).img);
end

% randomize and choose training set
examples = examples(randperm(length(examples)));

TRAINING_SET_FRAC = .75;
training_set_size = floor(TRAINING_SET_FRAC*length(examples));
training_set = examples(1:training_set_size);
test_set = examples(training_set_size+1:end);

svm = svmtrain([training_set.X]', [training_set.y], 'boxconstraint', .001, 'tolkkt', 1e-5);

% test
num_errors = 0;
for i=1:length(test_set)
  y_classifier = svmclassify(svm, test_set(i).X');
  y_true = test_set(i).y;
  if y_classifier ~= y_true
    num_errors = num_errors + 1;
    fprintf('error: %d, true: %d\n', y_classifier, y_true);
    test_set(i).X
    figure; imshow(test_set(i).img);
  end
end
fprintf('%d errors out of %d. %f%%\n', num_errors, length(test_set), 100*num_errors/length(test_set));

% save classifier
save(CLASSIFIER_OUTPUT, 'svm');
