close all;
VIDEO_FILE = '/Users/jonathan/Downloads/output.mp4';
OUTPUT = '/Users/jonathan/Downloads/output.mp4.mat';

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'uint8');

num = 0;

tic;
frames = {};
while ~isDone(video_source)
  frame = step(video_source);
  frames{end+1} = frame;
  num = num + 1;
  fprintf('%d\n', num);
end
toc;

fprintf('Total number of frames: %d\n', num);

save(OUTPUT, 'frames', '-v7.3');
