function [] = label_video()
close all;
%VIDEO_FILE = '/Users/jonathan/Downloads/output.mp4';
VIDEO_FILE_MAT = '/Users/jonathan/Downloads/output.mp4.mat';
SCALE = 1;
%FRAME_SKIP = 10;

%video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');
video = load(VIDEO_FILE_MAT); video = video.frames;

figure;
h = LabelDataHandle;
  function [] = on_exit(data_handle)
    boxes = data_handle.boxes; frames = data_handle.frames;
    save(Cfg.LABEL_FILE, 'boxes', 'frames');
    fprintf('Saved to %s\n', Cfg.LABEL_FILE);
  end
cleanup_obj = onCleanup(@() on_exit(h));

for i=1:length(video)
  frame = imresize(video{i}, SCALE);

  imshow(frame);
  pt = round(getPosition(impoint));

  fprintf('Frame %d/%d (%f%%)\n', i, length(video), 100*i/length(video));
%   fprintf('%d, %d\n', pt(2), .9*size(frame,1));
  
  if pt(2) < .9*size(frame,1)
    box = [floor(pt(1) - Cfg.PATCH_SIZE/2), floor(pt(2) - Cfg.PATCH_SIZE/2), Cfg.PATCH_SIZE-1, Cfg.PATCH_SIZE-1];
%     imrect(gca, box);
    h.boxes = [h.boxes; box];
    h.frames{end+1} = frame;
    fprintf('saved\n');
  else
    fprintf('skipped\n');
  end
end

end
