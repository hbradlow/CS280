clear; clc; close all;

VIDEO_FILE = '/Users/jonathan/Desktop/textons.MOV';
POS_OUTPUT_DIR = 'out/training/pos';
NEG_OUTPUT_DIR = 'out/training/neg';
SCALE = .3;
FRAME_SKIP = 10;
PATCH_SIZE = 40;
NUM_NEG_EXAMPLES_PER_POS = 10;

video_source = vision.VideoFileReader(VIDEO_FILE, 'ImageColorSpace', 'RGB', 'VideoOutputDataType', 'double');

figure;
curr_frame = 0;
while ~isDone(video_source)
  frame = imresize(step(video_source), SCALE); curr_frame = curr_frame + 1;

  imshow(frame);
  box = round(getPosition(imrect));
  
  p = to_square_patch(imcrop(frame, box), PATCH_SIZE);
  imwrite(p, sprintf('%s/img_%d.png', POS_OUTPUT_DIR, curr_frame));
  
  for i=1:NUM_NEG_EXAMPLES_PER_POS
    while 1
      sx = randi(size(frame, 2) - PATCH_SIZE); sy = randi(size(frame, 1) - PATCH_SIZE);
      negbox = [sx sy PATCH_SIZE PATCH_SIZE];
      if rectint(box, negbox) == 0
        break
      end
    end
    p = imcrop(frame, negbox);
    imwrite(p, sprintf('%s/img_%d_%d.png', NEG_OUTPUT_DIR, curr_frame, i));
  end

  for i=1:FRAME_SKIP
    step(video_source); curr_frame = curr_frame + 1;
  end
end

release(video_source);
