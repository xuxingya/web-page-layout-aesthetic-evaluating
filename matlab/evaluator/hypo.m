function h = hypo( theta, x )
%HYPO Summary of this function goes here
%   the hypothesis of the logisticRegression
%   x could be a vector or matrix whose dim is m*n m for number of sample
%   n for number of features
h = 1./(1 + exp(-x*theta));
end