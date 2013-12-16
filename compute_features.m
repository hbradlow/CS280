function [ out ] = compute_features(orig_p)

NUM_HIST_BINS = 25;
filters = load('out/training/filters.mat'); filters = filters.out;
total_dim = NUM_HIST_BINS + size(filters, 1);

out = zeros(total_dim, 1);

% hue histogram
p = double(orig_p);
mean_p = mean(p(:));
normed_p = (p - mean_p)/std(p(:)) + mean_p;

hsv = rgb2hsv(normed_p);
[counts, ~] = imhist(hsv(:,:,1), NUM_HIST_BINS);
out(1:NUM_HIST_BINS) = counts/sum(counts);

% responses to filters
gray = rgb2gray(orig_p);
out(NUM_HIST_BINS+1:end) = pdist2(gray(:)', filters, 'correlation');

end
