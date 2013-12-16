clear; clc; close all;

VIDEO_FILE = '/Users/kevinlindkvist/Downloads/bucket.mp4';
OUTPUT_DIR = 'out/training/neg';
PATCH_SIZE = 40;
SCALE = 1;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
curr_frame = 0;
while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); curr_frame = curr_frame + 1;
  
  for i = 1:2
    sx = randi(size(frame, 2) - PATCH_SIZE); sy = randi(size(frame, 1) - PATCH_SIZE);
    negbox = [sx sy PATCH_SIZE PATCH_SIZE];
  
    p = imcrop(frame, negbox);
   
    imwrite(p, sprintf('%s/img_%d_%d.png', OUTPUT_DIR, curr_frame, i));
  end
  
  step(video_source); curr_frame = curr_frame + 1;
  
end