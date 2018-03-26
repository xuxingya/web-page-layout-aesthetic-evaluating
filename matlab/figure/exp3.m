addpath('utils');
load('data/exp2.mat');

badFeatures = features(labels==0,:);
goodFeatures = features(labels==2,:);

len = size(goodFeatures);
%bs = len(2)/3;
bs = 4;
cn = 2;

for di = (1:cn-1)
    for dj = (di+1:cn)
        for dk = (1:bs)
            i = (di-1)*bs+dk;
            j = (dj-1)*bs+dk;
            h = figure;
            set(h,'name', [num2str(i),',',num2str(j)]);

            plot(badFeatures(:,i),badFeatures(:,j), 'o', 'color', 'red');
            hold

            plot(goodFeatures(:,i),goodFeatures(:,j), '+', 'color', 'blue');
        end
    end
end