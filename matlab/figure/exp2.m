addpath('utils');
load('data/exp2.mat');

badFeatures = features(labels==0,:);
goodFeatures = features(labels==2,:);

len = (size(goodFeatures));

for i = (1:len(2))
%for i = (1)
    fn = i;
    figure;
    [a,x] = ksdensity(goodFeatures(:, fn));
    H1 = plot(x,a, 'blue');
    hold

    [a,x] = ksdensity(badFeatures(:,fn));
    H2 = plot(x,a, 'red');
    legend([H1, H2],'good', 'bad');
    title(featureNames(i,:));
    ylabel('probability');
    
end