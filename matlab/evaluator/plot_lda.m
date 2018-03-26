
P = exp(L) ./ repmat(sum(exp(L),2),[1 2]);
Lg = P(labels==1,:);
Lb = P(labels==0,:);


hold on;
plot(Lg(:,1), Lg(:,2), '+', 'color', 'blue');
plot(Lb(:,1), Lb(:,2), 'o', 'color', 'red');
hold off;