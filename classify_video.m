clear; clc; close all;

VIDEO_FILE_MAT = '/Users/jonathan/Downloads/test2.mp4.mat';
SCALE = 1;
FRAME_SKIP = 1;

%video_source = vision.VideoFileReader(VIDEO_FILE_MAT, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
video = load(VIDEO_FILE_MAT); video = video.frames;
player = vision.VideoPlayer('Name', 'Colored Hat Detection');
svm = load(Cfg.CLASSIFIER_FILE); svm = svm.svm;

all_detected_points = [];

for frame_idx=1:FRAME_SKIP:length(video)
  frame = imresize(video{frame_idx}, SCALE); %curr_frame = curr_frame + 1;
  result = frame;

  fprintf('got frame\n');
  
  WINDOW_SKIP = 20;
  total = 0;
  for i=1:WINDOW_SKIP:size(frame, 2)-Cfg.PATCH_SIZE
    for j=1:WINDOW_SKIP:size(frame, 1)-Cfg.PATCH_SIZE
      total = total + 1;
    end
  end
  patch_features = zeros(total, length(compute_features(frame(1:Cfg.PATCH_SIZE,1:Cfg.PATCH_SIZE,:))));
  prerejected = zeros(total, 1);
  curr = 0;
  for i=1:WINDOW_SKIP:size(frame, 2)-Cfg.PATCH_SIZE
    for j=1:WINDOW_SKIP:size(frame, 1)-Cfg.PATCH_SIZE
      curr = curr + 1;
      p = frame(j:j+Cfg.PATCH_SIZE-1,i:i+Cfg.PATCH_SIZE-1,:);
      patch_features(curr,:) = compute_features(p)';
      prerejected(curr) = prereject(p);
    end
  end
  svm_results = svmclassify(svm, patch_features);
  curr = 0;
  detected_points = [];
  for i=1:WINDOW_SKIP:size(frame, 2)-Cfg.PATCH_SIZE
    for j=1:WINDOW_SKIP:size(frame, 1)-Cfg.PATCH_SIZE
      curr = curr + 1;
      %if svm_results(curr) == 1 && prerejected(curr) == 0
      if prerejected(curr) == 0
        result = insertShape(result, 'Rectangle', [i j Cfg.PATCH_SIZE Cfg.PATCH_SIZE], 'Color', 'red');
        
        % median of centers of boxes
        center = [(i + i+Cfg.PATCH_SIZE-1)/2, (j + j+Cfg.PATCH_SIZE-1)/2];
        detected_points = [detected_points; center];
      end
    end
  end
  if length(detected_points) > 0
    median_center = median(detected_points, 1);
    result = insertShape(result, 'FilledCircle', [median_center 10], 'Color', 'green');
    all_detected_points = [all_detected_points; median_center];
  end
  
  
  
%   patches = im2col(frame, [Cfg.PATCH_SIZE Cfg.PATCH_SIZE], 'sliding')';
%   fprintf('done with im2col\n');
%   tmp = compute_features(patches(1,:));
%   features = zeros(size(patches, 1), size(tmp, 1));
%   fprintf('patchifying\n');
%   for i=1:size(patches, 1)
%     features(i,:) = compute_features(patches(i,:));
%   end
%   frptinf('done\n');
%   y = svmclassify(svm, features);
%   y_im = col2im(results, [Cfg.PATCH_SIZE Cfg.PATCH_SIZE], [size(frame,1) size(frame,2)]);
%   
%   result(y_im == 1) = [255 0 0];
  
%   for i=1:SKIP:size(frame, 2)-Cfg.PATCH_SIZE
%     for j=1:SKIP:size(frame, 1)-Cfg.PATCH_SIZE
%       box = [i j Cfg.PATCH_SIZE Cfg.PATCH_SIZE];
%       p = imcrop(frame, box);
%       p = p(1:Cfg.PATCH_SIZE,1:Cfg.PATCH_SIZE,:);
%       patches = 
%       if svmclassify(svm, compute_features(window)') == 1
%         result = insertShape(result, 'Rectangle', [i j Cfg.PATCH_SIZE Cfg.PATCH_SIZE], 'Color', 'green');
%       end
%     end
%   end
  fprintf('showed frame!\n');
  step(player, result);

end

save('out/test/classified_points_only_thresh.mat', 'all_detected_points');

%release(video_source);
release(player);
