function [aveScores] = getScore(features, labels, select, alpha)
%test datajoin by gradient ascent 
%load('datajoin.mat');
%load('select.mat');

data = features(:,select');
label = labels;
label(label==2) = 1;
label = double(label);
m = size(data,1);%the number of sample
K = 5;%K fold
scoresMat = zeros(K,3);
indices = crossvalind('Kfold',m,K);

for i = 1:K
    test=(indices==i);
    train=~test;
    data_train=data(train,:);
    label_train=label(train,:);
    data_test=data(test,:);
    label_test=label(test,:);
    theta=logR2(data_train,label_train, alpha, 0.5);
    [scoresMat(i,1), scoresMat(i,2), scoresMat(i,3)]=predict(data_test,label_test,theta);
end

aveScores=sum(scoresMat)/K;
fprintf('the average allscores is %f \n', aveScores(1));
fprintf('the average scores0 is %f \n', aveScores(2));
fprintf('the average scores1 is %f \n', aveScores(3));

end
