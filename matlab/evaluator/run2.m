labels(labels==2)=1;
labels = double(labels);


oo = ones(364,1);
oo(3) = 0;
oo = logical(oo);
X = features(oo, :);
Y = labels(oo, :);

n = size(X,2);%the number of features
m = size(X,1);%the number of sample
theta = zeros(n,1);
lold = 0;
alpha = 0.0001;
para = 0.1;
while(true)
  [l, gradient] = costFunction(X, Y, theta, para);
  theta = theta + alpha * gradient;
  if(lold~=0 && abs(l-lold)/abs(lold)<0.0000001)
      break;
  end
  lold = l;
end

select = abs(theta)>2.8;
dt = logR2(X(:,select'), Y, 0.003, 0.5);
save theta.117.mat theta;
save dt.117.mat dt;
%run;