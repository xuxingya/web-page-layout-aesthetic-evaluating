load theta.features.mat;

X = features;
Y = labels;
sel = 1:0.1:4;
ax = 0.001:0.001:0.005;

best_b = [];
best_s = [];
best_i = [];

for i=1:length(sel)
    select = abs(theta)>sel(i);
    scores = [];

    for alpha= ax
        score=getScore(X, Y, select, alpha);
        scores = [scores score(1)];
    end

    [b, ix] = max(scores);
    best_b = [best_b b];
    best_s = [best_s; scores];
    best_i = [best_i ix];
end

[bbb, ix] = max(best_b);
bs = best_s(ix,:);
i = best_i(ix);

fprintf('the best score is %f \n', bbb);
fprintf('the best alpha is %f \n', ax(i));
fprintf('the best sel is %f \n', sel(ix));