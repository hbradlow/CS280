function [] = main()

fprintf('train\n'); train;
fprintf('classify_video\n'); out = classify_video();

truth = load('/Users/jonathan/code/CS280/out/test/points.mat'); truth = truth.points;

mean_err = mean(sqrt(sum((out - truth).^2, 2)));
fprintf('mean error: %f\n', mean_err);

end
