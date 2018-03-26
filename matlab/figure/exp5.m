addpath('utils');
load('data/exp10.mat');

badFeatures = features(labels==0,:);
goodFeatures = features(labels==2,:);

len = (size(goodFeatures));

for sp=0.25:0.01:0.4
%sp = 0.38;

for i = (1)
%for i = (21)
    fn = i;
    figure;
    %[a,x] = ksdensity(goodFeatures(goodFeatures(:, fn)<sp, fn));
    %plot(x,a, 'blue');
    selected_good = sum(goodFeatures(:, fn)<sp);
    selected_bad = sum(badFeatures(:, fn)<sp);
    sb = size(badFeatures);
    sg = size(goodFeatures);
    b = bar([selected_good(1)*1.0/sg(1) selected_bad(1)*1.0/sb(1);]);
    ch = get(b,'children');
    set(ch,'FaceVertexCData',[1;2]);
    set(gca,'XTickLabel',{'good','bad',});
    ylabel('probability');
    %hold

    %[a,x] = ksdensity(badFeatures(badFeatures(:, fn)<sp, fn));
    %plot(x,a, 'red');
end
end