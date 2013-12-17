function [ out ] = compute_features(orig_p)

out = [];

hsv = rgb2hsv(orig_p);

% hue histogram
if Cfg.FEATURES_HUE
  [counts, ~] = imhist(hsv(:,:,1), Cfg.NUM_HIST_BINS);
  hue_hist = counts/sum(counts);
  out = [out; hue_hist];
end

% saturation histogram
if Cfg.FEATURES_SAT
  [counts, ~] = imhist(hsv(:,:,2), Cfg.NUM_HIST_BINS);
  sat_hist = counts/sum(counts);
  out = [out; sat_hist];
end

% hog
if Cfg.FEATURES_HOG
  hog = HoG(double(orig_p));
  out = [out; hog];
end

end
