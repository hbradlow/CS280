pos_folder = '/Users/jonathan/code/CS280/training_data/positive';
neg_folder = '/Users/jonathan/code/CS280/training_data/negative';


trainCascadeObjectDetector('hat_detector.xml', pos_folder, neg_folder, 'FalseAlarmRate', 0.2, 'NumCascadeStages', 5);
%detector = vision.CascadeObjectDetector('hat_detector.xml');

