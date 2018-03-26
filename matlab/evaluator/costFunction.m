function [jVal, gradient] = costFunction(features, labels, theta, para)
xl = features;
yl = labels;
n = size(xl,2);%the number of features
m = size(xl,1);%the number of sample
%get the gradient of likehood(theta)
    grad = sum(repmat(yl-hypo(theta, xl), 1, n).*xl);
    grad = grad';
    gradient = grad - para*regulargrad(theta);
  jVal = -likehood(theta, xl, yl)/m + para*regular(theta)/m ;
  fprintf('norm(grad) is %f, the cost is %f \n', norm(grad), jVal);
end
