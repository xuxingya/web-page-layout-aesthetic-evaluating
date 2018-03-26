function [ theta ] = logR2( features, labels, alpha, threshold )
%logistic Regression %alpha is the speed of converge
%by batch gradient ascent
xl = features;
yl = labels;

n = size(xl,2);%the number of features
%m = size(xl,1);%the number of sample
theta = zeros(n,1);
%alpha = 0.1;%the speed of converge
%the Hessian matrix
%H = zeros(length(features(1,:)), length(features(1,:)));
lold = 0;
while(true)
%get the gradient of likehood(theta)
    grad = sum(repmat(yl-hypo(theta, xl), 1, n).*xl);
    grad = grad';
    
   theta = theta + alpha * grad;
   m = size(features, 1);
  l = -likehood(theta, xl, yl)/m;
  fprintf('norm(grad) is %f, likehood(theta) is %f \n', norm(grad), l);
  if(lold~=0 && abs(l-lold)/abs(lold)<0.00001)
      break;
  end
    if norm(grad)<threshold
        break;
    end
    lold = l;
end

end
