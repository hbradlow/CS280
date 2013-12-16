clear; clc; close all;

POS_EXAMPLES_DIR = 'out/training/pos';
NEG_EXAMPLES_DIR = 'out/training/neg';
CLASSIFIER_OUTPUT = 'out/training/classifier.mat';
PATCH_SIZE = 40;

trans_nums = [5 10 15];
translations = { maketform('affine', eye(3)) };
%   zooms = linspace(1, 2, 5);
zooms = [1];
for tx=trans_nums
  for ty=trans_nums
    translations{end+1} = maketform('affine', [1 0 tx; 0 1 ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 -tx; 0 1 ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 -tx; 0 1 -ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 tx; 0 1 -ty; 0 0 1]');
  end
end

% load all examples and compute features
examples = struct('img', {}, 'X', {}, 'y', {});
num_pos = 0; num_neg = 0;
for file=dir([POS_EXAMPLES_DIR '/*.png'])'
  i = length(examples) + 1;
  im = imread([POS_EXAMPLES_DIR '/' file.name]);
  examples(i).img = im;
  examples(i).y = 1;
  
  
  % jitter positive examples
  fprintf('Making filters\n');

  for t=1:length(translations)
    translated_filter = imtransform(im, translations{t}, 'XData', [1 PATCH_SIZE], 'YData', [1 PATCH_SIZE]);
    for z=zooms
      zoomed_filter = imresize(translated_filter, z);
      crop_start = floor(size(zoomed_filter, 1)/2 - PATCH_SIZE/2)+1;
%       cropped = imcrop(zoomed_filter, [crop_start crop_start PATCH_SIZE PATCH_SIZE]);
      cropped = zoomed_filter(crop_start:crop_start+PATCH_SIZE-1, crop_start:crop_start+PATCH_SIZE-1, :);
      i = length(examples) + 1;
      examples(i).img = cropped;%(1:PATCH_SIZE,1:PATCH_SIZE,:);
      examples(i).y = 1;
    end
  end 
end


Z = zeros(PATCH_SIZE, PATCH_SIZE, 3, length(examples));
for i=1:length(examples)
  Z(:,:,:,i) = examples(i).img;
end
figure; montage(Z);


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
