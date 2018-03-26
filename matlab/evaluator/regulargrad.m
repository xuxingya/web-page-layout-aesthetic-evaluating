function [ grad ] = regulargrad( theta )
grad = zeros(size(theta));
grad(theta>=0.2) = 1;
grad(theta<=-0.2) = -1;
grad(abs(theta)<0.2) = 10*theta(abs(theta)<0.2);
end

