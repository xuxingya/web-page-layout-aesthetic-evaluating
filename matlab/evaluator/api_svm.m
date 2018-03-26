function result = api_svm( args )
%API Summary of this function goes here
%   Detailed explanation goes here

features = args.feature;
load theta.117.mat;
load svm.117.mat;

select = abs(theta)>1.7;
f = features(:, select');

result = svmclassify(svmStruct, f);


end

