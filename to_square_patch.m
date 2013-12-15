function [ out ] = to_square_patch(im, target_size)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

if size(im, 1) < size(im, 2)
  im_resized = imresize(im, [target_size NaN]);
  a = floor(size(im_resized, 2)/2. - target_size/2.);
  out = imcrop(im_resized, [1 a target_size target_size]);
else
  im_resized = imresize(im, [NaN target_size]);
  a = floor(size(im_resized, 1)/2. - target_size/2.);
  out = imcrop(im_resized, [a 1 target_size target_size]);
end

end