% SVMÊµÑé
oo = ones(364,1);
oo(349) = 0;
oo = logical(oo);
X = features(oo,:);
Y = labels(oo,:);

KF = 'rbf';

xk = 0.1:0.2:8;
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
        
        svmStruct = svmtrain(data_train, label_train, 'kernel_function', KF, 'rbf_sigma', k);
        class = svmclassify(svmStruct, data_test);
        classperf(cp,class,test); 
    end

    yc = [yc cp.CorrectRate];
end

%plot(xk, yc, 'b');
[b, ix] = max(yc);

xk(ix)
b
