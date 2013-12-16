clear; clc; close all;

VIDEO_FILE = '/Users/jonathan/Downloads/output.mp4';
SCALE = 1;
FRAME_SKIP = 30;
PATCH_SIZE = 40;

detector = vision.CascadeObjectDetector('cascade.xml');

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
player = vision.VideoPlayer('Name', 'Colored Hat Detection');

while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); %curr_frame = curr_frame + 1;

  bboxes = step(detector, frame);
  result = insertObjectAnnotation(frame, 'rectangle', bboxes, 'hat');
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
