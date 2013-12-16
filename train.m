clear; clc; close all;

%% Load all examples
examples = struct('img', {}, 'X', {}, 'y', {});
for file=dir([Cfg.POS_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  im = imread([Cfg.POS_EXAMPLES_DIR '/' file.name]);
  examples(i).img = im;
  examples(i).y = 1;
end

% Z = zeros(PATCH_SIZE, PATCH_SIZE, 3, length(examples));
% for i=1:length(examples)
%   Z(:,:,:,i) = examples(i).img;
% end
% figure; montage(Z);

for file=dir([Cfg.NEG_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  examples(i).img = imread([Cfg.NEG_EXAMPLES_DIR '/' file.name]);
  examples(i).y = -1;
end

%% Compute features
for i=1:length(examples)
  examples(i).X = compute_features(examples(i).img);
end

%% Randomize and split training/test sets
examples = examples(randperm(length(examples)));

training_set_size = floor(Cfg.TRAINING_SET_FRAC*length(examples));
training_set = examples(1:training_set_size);
test_set = examples(training_set_size+1:end);

%% Train
svm = svmtrain([training_set.X]', [training_set.y], 'boxconstraint', .001, 'tolkkt', 1e-5);

%% Test
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

%% Save classifier
save(Cfg.CLASSIFIER_FILE, 'svm');
