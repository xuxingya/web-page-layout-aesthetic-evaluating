% PCA + KNN


topKs = [];
scores = [];
ks = [];
dKs = [];

for k = 0.90:0.01:0.98; % 设定表达能力阈值

    [pc,score,latent] = princomp(features);
    topK = 0;

    for i=1:length(latent)
        if(sum(latent(1:i))/sum(latent)>k)
            sum(latent(1:i))/sum(latent);
            topK = i;
            break;
        end
    end

    topKs = [topKs topK];
    ks = [ks k];
    convertM = pc(:,1:topK);
    
    X = features * convertM;
    Y = labels;

    d = 'euclidean';

    xk = 1:5:100;
    yc = [];

    for dk=xk
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

            class = knnclassify(data_test, data_train, label_train, dk, d);
            classperf(cp,class,test); 
        end

        yc = [yc cp.CorrectRate];
    end

    [b, ix] = max(yc);
    scores = [scores b];
    dKs = [dKs xk(ix)];
end

plot( 0.90:0.01:0.98, scores);
[b, ix] = max(scores);
fprintf('best rate is %f \n', ks(ix));
fprintf('best topk is %d \n', topKs(ix));
fprintf('best k is %d \n', dKs(ix));
fprintf('best score is %f \n', scores(ix));