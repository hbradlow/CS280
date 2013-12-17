function [ out ] = prereject(p)

out = 1;

hsv = rgb2hsv(p);
hue = hsv(:,:,1);
mean_hue = median(hue(:));
if .15 < mean_hue && mean_hue < .35
  out = 0;
end

end
