clear; clc; close all;

%% Load all examples
pos_files = dir([Cfg.POS_EXAMPLES_DIR '/*.png'])';
neg_files = dir([Cfg.NEG_EXAMPLES_DIR '/*.png'])';

examples = struct('img', {}, 'X', {}, 'y', {});

bar = waitbar(0, 'Loading images');

for file=dir([Cfg.POS_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  im = imread([Cfg.POS_EXAMPLES_DIR '/' file.name]);
  if size(im, 1) ~= Cfg.PATCH_SIZE || size(im, 2) ~= Cfg.PATCH_SIZE
    fprintf('skipped\n');
    continue
  end
  examples(i).img = im;
  examples(i).y = 1;
  waitbar(i/(length(pos_files)+length(neg_files)), bar);
end

for file=dir([Cfg.NEG_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  im = imread([Cfg.NEG_EXAMPLES_DIR '/' file.name]);
  if size(im, 1) ~= Cfg.PATCH_SIZE || size(im, 2) ~= Cfg.PATCH_SIZE
    fprintf('skipped\n');
    continue
  end
  examples(i).img = im;
  examples(i).y = -1;
  waitbar((i+length(pos_files))/(length(pos_files)+length(neg_files)), bar);
end

close(bar);

fprintf('Loaded %d positive and %d negative examples\n', length(pos_files), length(neg_files));

%% Compute features
box = waitbar(0, 'Computing features');
for i=1:length(examples)
  examples(i).X = compute_features(examples(i).img);
  waitbar(i/length(examples), box);
end
close(box);

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
    figure; imshow(test_set(i).img);
  end
end
fprintf('%d errors out of %d. %f%%\n', num_errors, length(test_set), 100*num_errors/length(test_set));

%% Save classifier
save(Cfg.CLASSIFIER_FILE, 'svm');
