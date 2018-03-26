% KNNÊµÑé
X = features;
Y = labels;

d = 'euclidean';

xk = 1:5:100;
yc = [];

for k=xk
    cp = classperf(Y); % initializes the CP object

    ck = 5;
    indices = crossvalind('Kfold', length(X), ck);
    for i = 1:ck
        test=(indices==i);
        train=~test;
        data_train=X(train,:);
        label_train=Y(train,:);
        data_test=X(test,:);
        label_test=Y(test,:);

        class = knnclassify(data_test, data_train, label_train, k, d);
        classperf(cp,class,test); 
    end

    yc = [yc cp.CorrectRate];
end

plot(xk, yc, 'g');
[b, ix] = max(yc);

xk(ix)
b
