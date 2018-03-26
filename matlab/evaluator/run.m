%Logistic Regression + LASSO

sel = 1:0.1:4;
scoresMat=zeros(length(sel),3);
for i=1:length(sel)
    select = abs(theta)>sel(i);
    scoresMat(i,:)=getScore(features, labels, select, 0.003);
end

figure;
plot(sel,scoresMat(:,1)','r+');
hold on;
plot(sel,scoresMat(:,2)','go');
hold on;
plot(sel,scoresMat(:,3)','b*');

[b, ix] = max(scoresMat(:,1));
sel(ix)
b