clear; clc; close all;

VIDEO_FILE = '/Users/jonathan/Desktop/textons.MOV';
OUTPUT_FILE = 'out/training/labels.mat';
SCALE = .3;
FRAME_SKIP = 10;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');

figure;
curr_frame = 0;
boxes = []; frames = {};
while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); curr_frame = curr_frame + 1;

  imshow(frame);
  box = round(getPosition(imrect));
  
  boxes = [boxes; box];
  frames{end+1} = frame;
  save(OUTPUT_FILE, 'boxes', 'frames');

  for i=1:FRAME_SKIP
    step(video_source); curr_frame = curr_frame + 1;
  end
end

release(video_source);
