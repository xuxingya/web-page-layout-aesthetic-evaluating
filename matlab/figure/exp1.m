
addpath('utils');
load('data/exp_global.mat');

badFeatures = features(labels==0,:);
goodFeatures = features(labels==2,:);

ranges = 0:0.05:1;

figure;
draw_hist(badFeatures, ranges);
figure(2);
draw_hist(goodFeatures, ranges);