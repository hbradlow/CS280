clear; clc; close all;

LABEL_FILE = 'out/training/labels.mat';
FILTERS_OUTPUT_FILE = 'out/training/filters.mat';
NUM_NEG_EXAMPLES_PER_POS = 10;
NUM_FILTERS = 100;

labels = load(LABEL_FILE);

%% Extract positive and negative patches from user-labeled regions
fprintf('Extracting patches\n');
for i=1:length(labels.frames)
  box = labels.boxes(i,:);
  frame = labels.frames{i};
  
  p = to_square_patch(imcrop(frame, box), Cfg.PATCH_SIZE);
  imwrite(p, sprintf('%s/img_%d.png', Cfg.POS_OUTPUT_DIR, i));
  
  for j=1:NUM_NEG_EXAMPLES_PER_POS
    while 1
      sx = randi(size(frame, 2) - Cfg.PATCH_SIZE); sy = randi(size(frame, 1) - Cfg.PATCH_SIZE);
      negbox = [sx sy Cfg.PATCH_SIZE Cfg.PATCH_SIZE];
      if rectint(box, negbox) == 0
        break
      end
    end
    p = imcrop(frame, negbox);
    p = p(1:Cfg.PATCH_SIZE, 1:Cfg.PATCH_SIZE, :);
    imwrite(p, sprintf('%s/img_%d_%d.png', Cfg.NEG_OUTPUT_DIR, i, j));
  end
end



  
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
  % jitter positive examples
  fprintf('Making filters\n');

  for t=1:length(translations)
    translated_filter = imtransform(im, translations{t}, 'XData', [1 Cfg.PATCH_SIZE], 'YData', [1 Cfg.PATCH_SIZE]);
    for z=zooms
      zoomed_filter = imresize(translated_filter, z);
      crop_start = floor(size(zoomed_filter, 1)/2 - Cfg.PATCH_SIZE/2)+1;
%       cropped = imcrop(zoomed_filter, [crop_start crop_start Cfg.PATCH_SIZE Cfg.PATCH_SIZE]);
      cropped = zoomed_filter(crop_start:crop_start+Cfg.PATCH_SIZE-1, crop_start:crop_start+Cfg.PATCH_SIZE-1, :);
      i = length(examples) + 1;
      examples(i).img = cropped;%(1:Cfg.PATCH_SIZE,1:Cfg.PATCH_SIZE,:);
      examples(i).y = 1;
    end
  end 












%% Create filters from positive examples
fprintf('Making filters\n');
trans_nums = [5 10];
translations = { maketform('affine', eye(3)) };
%zooms = [linspace(.2, .91, 9) linspace(1, 5, 10)];
zooms = linspace(1, 2, 5);
for tx=trans_nums
  for ty=trans_nums
    translations{end+1} = maketform('affine', [1 0 tx; 0 1 ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 -tx; 0 1 ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 -tx; 0 1 -ty; 0 0 1]');
    translations{end+1} = maketform('affine', [1 0 tx; 0 1 -ty; 0 0 1]');
  end
end

all_filters = {};
for i=1:length(labels.frames)
  box = labels.boxes(i,:);
  frame = labels.frames{i};
  
  orig_filter = rgb2gray(to_square_patch(imcrop(frame, box), Cfg.PATCH_SIZE));
  orig_filter = (orig_filter - mean(orig_filter(:)))/(std(orig_filter(:))+.001);
  
  for t=1:length(translations)
    %bounds = findbounds(translations{t}, [1 1; size(orig_filter)]); bounds(1,:) = [1 1];
    %translated_filter = imtransform(orig_filter, translations{t}, 'XData', bounds(:,2)', 'YData', bounds(:,1)');
    translated_filter = imtransform(orig_filter, translations{t}, 'XData', [1 Cfg.PATCH_SIZE], 'YData', [1 Cfg.PATCH_SIZE]);
    %figure; imshow(translated_filter)

    for z=zooms
      zoomed_filter = imresize(translated_filter, z);
      crop_start = floor(size(zoomed_filter, 1)/2 - Cfg.PATCH_SIZE/2);
      cropped = imcrop(zoomed_filter, [crop_start crop_start Cfg.PATCH_SIZE Cfg.PATCH_SIZE]);
      all_filters{end+1} = cropped(1:Cfg.PATCH_SIZE,1:Cfg.PATCH_SIZE);
    end

  end
end

out = zeros(0, Cfg.PATCH_SIZE*Cfg.PATCH_SIZE);
count = 0;
for i=randperm(length(all_filters))
  x = all_filters{i};
  out(end+1,:) = x(:);
  count = count + 1;
  if count > NUM_FILTERS
    break;
  end
end

% out = zeros(length(all_filters), Cfg.PATCH_SIZE*Cfg.PATCH_SIZE);
% for i=1:length(all_filters)
%   x = all_filters{i};
%   out(i,:) = x(:);
% end

Z = zeros(Cfg.PATCH_SIZE, Cfg.PATCH_SIZE, 1, size(out, 1));
for i=1:size(out,1)
  Z(:,:,1,i) = reshape(out(i,:), Cfg.PATCH_SIZE, Cfg.PATCH_SIZE);
end
figure; montage(Z);


save(FILTERS_OUTPUT_FILE, 'out');
