function [ out ] = compute_features(orig_p)

% filters = load('out/training/filters.mat'); filters = filters.out;
% if size(orig_p,1) ~= 40 || size(orig_p,2) ~= 40
%   size(orig_p)
% end
orig_p = orig_p(1:Cfg.PATCH_SIZE,1:Cfg.PATCH_SIZE,:);

% hue histogram
p = double(orig_p);
mean_p = mean(p(:));
normed_p = (p - mean_p)/(std(p(:))+.001) + mean_p;

hsv = rgb2hsv(normed_p);
[counts, ~] = imhist(hsv(:,:,1), Cfg.NUM_HIST_BINS);
hue_hist = counts/sum(counts);
% out(1:NUM_HIST_BINS) = counts/sum(counts);

% saturation histogram
[counts, ~] = imhist(hsv(:,:,2), Cfg.NUM_HIST_BINS);
sat_hist = counts/sum(counts);

% responses to filters
% gray = double(rgb2gray(orig_p));
% out(NUM_HIST_BINS+1:end) = pdist2(gray(:)', filters, 'correlation');

%
hog = HOG(orig_p);
% out = hue_hist;
out = [hue_hist; sat_hist; hog];
% out = double(orig_p(:));

end
