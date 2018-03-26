addpath('utils');
load('data/exp6.mat');

cn = 100;
fr = 1:11;

goodFeatures = features(labels==2,:);
%sample = features(7764,:); % nav
sample = features(7769,:); % btn

badFeatures = features(labels==0,:);

mdl = knnsearch(badFeatures(:, fr), sample(:, fr), 'k', cn);

nodes = badFeatures(mdl,:);
fn = 14;

sv = nodes(:, fn);

[a,x] = ksdensity(sv);

plot(x,a, 'red');
hold


mdl = knnsearch(goodFeatures(:, fr), sample(:, fr), 'k', cn);
nodes = goodFeatures(mdl,:);
sv = nodes(:, fn);

[a,x] = ksdensity(sv);
plot(x,a, 'blue');


% m1 = mean(sv);
% n1 = std(sv);
% 
% X = 0:0.01:1;
% Y = (1/sqrt(2*pi*n1))*exp((-1/2)*(X-m1).^2/n1^2);
% 
% figure
% plot(X,Y);
% xlabel('Saliency Digree');
% ylabel('Probability');
% axis([0 1 0 2.5]);
% 
% p = (1/sqrt(2*pi*n1))*exp((-1/2)*(sample(16)-m1).^2/n1^2);