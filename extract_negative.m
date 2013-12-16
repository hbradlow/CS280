clear; clc; close all;

VIDEO_FILE = '/Users/jonathan/Downloads/bucket.mp4';
OUTPUT_DIR = 'out/training/neg';
PATCH_SIZE = 40;
SCALE = 1;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
curr_frame = 0;
while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); curr_frame = curr_frame + 1;
  
  for i = 1:3
    sx = randi(size(frame, 2) - PATCH_SIZE); sy = randi(size(frame, 1) - PATCH_SIZE);
    negbox = [sx sy PATCH_SIZE PATCH_SIZE];
  
    p = imcrop(frame, negbox);
    p = p(1:PATCH_SIZE, 1:PATCH_SIZE, :);
   
    imwrite(p, sprintf('%s/neg_img_%d_%d.png', OUTPUT_DIR, curr_frame, i));
  end
  
  step(video_source); curr_frame = curr_frame + 1;
  
end