% KNN+lassoÊµÑé

%sel = 1:0.1:3.5;
sel = 1.6;
scores = [];
ks = [];
ycs = [];

for i=1:length(sel)
    select = abs(theta)>sel(i);
    X = features(:,select');
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

        yc = [cp.CorrectRate yc];
    end

    plot(xk, yc, 'k');
    ycs = [ycs; yc];
    [b, ix] = max(yc);

    ks = [ks xk(ix)];
    scores = [scores b];
end

[b, ix] = max(scores);
byc = ycs(ix, :);
%plot(xk, byc, 'y');
fprintf('best k is %d \n', ks(ix));
fprintf('best score is %f \n', b);
fprintf('best sel is %f \n', sel(ix));
