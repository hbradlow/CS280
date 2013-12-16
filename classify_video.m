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

  for i=1:50:size(frame, 2)-PATCH_SIZE
    for j=1:50:size(frame, 1)-PATCH_SIZE
      box = [i j PATCH_SIZE PATCH_SIZE];
      window = imcrop(frame, box);
      window = window(1:PATCH_SIZE,1:PATCH_SIZE,:);
      if svmclassify(svm, compute_features(window)') == 1
        result = insertShape(result, 'Rectangle', [i j PATCH_SIZE PATCH_SIZE], 'Color', 'green');
      end
    end
  end
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
