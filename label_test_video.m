function [] = label_test_video()
close all;
VIDEO_FILE_MAT = '/Users/jonathan/Downloads/test2.mp4.mat';
SCALE = 1;

video = load(VIDEO_FILE_MAT); video = video.frames;

figure;
h = LabelDataHandle;
  function [] = on_exit(data_handle)
    points = data_handle.boxes;
    TEST_POINTS_FILE = 'out/test/points.mat';
    save(TEST_POINTS_FILE, 'points');
    fprintf('Saved to %s\n', TEST_POINTS_FILE);
  end
cleanup_obj = onCleanup(@() on_exit(h));

for i=1:length(video)
  frame = imresize(video{i}, SCALE);

  imshow(frame);
  pt = round(getPosition(impoint));

  fprintf('Frame %d/%d (%f%%)\n', i, length(video), 100*i/length(video));
%   fprintf('%d, %d\n', pt(2), .9*size(frame,1));

  if pt(2) < .9*size(frame,1)
%     imrect(gca, box);
    h.boxes = [h.boxes; pt];
    fprintf('saved\n');
  else
    fprintf('skipped\n');
  end
end

end
