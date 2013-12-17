function [] = patch_stats()
close all;
VIDEO_FILE_MAT = '/Users/jonathan/Downloads/test2.mp4.mat';
SCALE = 1;

video = load(VIDEO_FILE_MAT); video = video.frames;

figure;

%for i=1:length(video)
i = 1;
while 1
  frame = imresize(video{i}, SCALE);

  imshow(frame);
  pt = round(getPosition(impoint));

  fprintf('Frame %d/%d (%f%%)\n', i, length(video), 100*i/length(video));
  
  box = [floor(pt(1) - Cfg.PATCH_SIZE/2), floor(pt(2) - Cfg.PATCH_SIZE/2), Cfg.PATCH_SIZE-1, Cfg.PATCH_SIZE-1];
  imrect(gca, box);
  
  patch = imcrop(frame, box);
  
  patch_hsv = rgb2hsv(patch);
  patch_hue = patch_hsv(:,:,1);
  fprintf('mean hue: %f\n', mean(patch_hue(:)));
end

end
