function [ out ] = compute_features(p)

NUM_HIST_BINS = 25;
total_dim = NUM_HIST_BINS;

out = zeros(total_dim, 1);

% hue histogram
hsv = rgb2hsv(p);
[counts, x] = imhist(hsv(:,:,1), NUM_HIST_BINS);
out(1:NUM_HIST_BINS) = counts;

end
