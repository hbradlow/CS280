clear; clc; close all;

VIDEO_FILE = '/Users/jonathan/Downloads/output.mp4';
CLASSIFIER_FILE = 'out/training/classifier.mat';
SCALE = 1;
FRAME_SKIP = 10;
PATCH_SIZE = 40;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
player = vision.VideoPlayer('Name', 'Colored Hat Detection');
svm = load(CLASSIFIER_FILE); svm = svm.svm;

while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); %curr_frame = curr_frame + 1;
  result = frame;

  fprintf('got frame\n');
  
  total = 0;
  for i=1:50:size(frame, 2)-PATCH_SIZE
    for j=1:50:size(frame, 1)-PATCH_SIZE
      total = total + 1;
    end
  end
  patch_features = zeros(total, length(compute_features(frame(1:PATCH_SIZE,1:PATCH_SIZE,:))));
  curr = 0;
  for i=1:50:size(frame, 2)-PATCH_SIZE
    for j=1:50:size(frame, 1)-PATCH_SIZE
      curr = curr + 1;
      p = frame(j:j+PATCH_SIZE-1,i:i+PATCH_SIZE-1,:);
      patch_features(curr,:) = compute_features(p)';
    end
  end
  svm_results = svmclassify(svm, patch_features);
  curr = 0;
  for i=1:50:size(frame, 2)-PATCH_SIZE
    for j=1:50:size(frame, 1)-PATCH_SIZE
      curr = curr + 1;
      if svm_results(curr) == 1
        result = insertShape(result, 'Rectangle', [i j PATCH_SIZE PATCH_SIZE], 'Color', 'green');
      end
    end
  end
  
  
%   patches = im2col(frame, [PATCH_SIZE PATCH_SIZE], 'sliding')';
%   fprintf('done with im2col\n');
%   tmp = compute_features(patches(1,:));
%   features = zeros(size(patches, 1), size(tmp, 1));
%   fprintf('patchifying\n');
%   for i=1:size(patches, 1)
%     features(i,:) = compute_features(patches(i,:));
%   end
%   frptinf('done\n');
%   y = svmclassify(svm, features);
%   y_im = col2im(results, [PATCH_SIZE PATCH_SIZE], [size(frame,1) size(frame,2)]);
%   
%   result(y_im == 1) = [255 0 0];
  
%   for i=1:50:size(frame, 2)-PATCH_SIZE
%     for j=1:50:size(frame, 1)-PATCH_SIZE
%       box = [i j PATCH_SIZE PATCH_SIZE];
%       p = imcrop(frame, box);
%       p = p(1:PATCH_SIZE,1:PATCH_SIZE,:);
%       patches = 
%       if svmclassify(svm, compute_features(window)') == 1
%         result = insertShape(result, 'Rectangle', [i j PATCH_SIZE PATCH_SIZE], 'Color', 'green');
%       end
%     end
%   end
  fprintf('showed frame!\n');
  step(player, result);

  for i=1:FRAME_SKIP
    if isDone(video_source)
      break;
    end
    frame = step(video_source); %curr_frame = curr_frame + 1;
  end
end

release(video_source);
release(player);
