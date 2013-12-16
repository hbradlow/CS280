function [] = label_video()
close all;
VIDEO_FILE = '/Users/jonathan/Downloads/output.mp4';
SCALE = 1;
FRAME_SKIP = 10;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');

figure;
curr_frame = 0;
boxes = []; frames = {};

  function [] = on_exit(data_handle)
    boxes = data_handle.boxes; frames = data_handle.frames;
    save(Cfg.LABEL_FILE, 'boxes', 'frames');
    fprintf('Saved to %s\n', Cfg.LABEL_FILE);
  end

cleanup_obj = onCleanup(@() on_exit(data_handle));

while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); curr_frame = curr_frame + 1;

  imshow(frame);
  box = round(getPosition(imrect));
  if box(3) ~= 0 && box(4) ~= 0
    boxes = [boxes; box];
    frames{end+1} = frame;
%     save(Cfg.OUTPUT_FILE, 'boxes', 'frames');
    fprintf('saved\n');
  else
    fprintf('skipped\n');
  end

  for i=1:FRAME_SKIP
    step(video_source); curr_frame = curr_frame + 1;
  end
end

end