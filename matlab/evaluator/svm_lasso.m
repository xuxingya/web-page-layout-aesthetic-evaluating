% SVM+lassoÊµÑé

oo = ones(364,1);
oo(349) = 0;
oo = logical(oo);

sel = 1:0.1:3.5;
scores = [];
ks = [];
ycs = [];


Y = labels(oo,:);

for i=1:length(sel)
    select = abs(theta)>sel(i);
    X = features(oo,select');

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

        yc = [cp.CorrectRate yc];
    end

    %plot(xk, yc, 'b');
    [b, ix] = max(yc);
    ycs = [ycs ; yc];

    ks = [ks xk(ix)];
    scores = [scores b];
end

svmStruct = svmtrain(X, Y, 'kernel_function', 'rbf', 'rbf_sigma', 1.1);

[b, ix] = max(scores);
fprintf('best k is %d \n', ks(ix));
fprintf('best score is %f \n', b);
fprintf('best sel is %f \n', sel(ix));
