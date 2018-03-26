addpath('utils');
load('data/exp10.mat');

badFeatures = features(labels==0,:);
goodFeatures = features(labels==2,:);

len = size(goodFeatures);
bs = len(2)/3;

for di=(1:2)
    for dj=(di+1:3)
        for dk=(1:bs)
            i = (di-1)*bs + dk;
            j = (dj-1)*bs + dk;
            h = figure;
            set(h,'name', [num2str(i),',',num2str(j)]);

            s = size(badFeatures);
            dx = [];
            for d=1:s(1)
                 dx = [dx; (badFeatures(d,i)+0.01)/(badFeatures(d,j)+0.01)];
            end;
            [a,x] = ksdensity(dx);
            plot(x,a, 'color', 'red');
            hold

            s = size(goodFeatures);
            dx = [];
            for d=1:s(1)
                dx = [dx; (goodFeatures(d,i)+0.01)/(goodFeatures(d,j)+0.01)];
            end;
            [a,x] = ksdensity(dx);
            plot(x, a, 'color', 'blue');
        end
    end
end