function result = api( args )
%API Summary of this function goes here
%   Detailed explanation goes here

features = args.feature;
load theta.117.mat;
load dt.117.mat;
select = abs(theta)>2.8;

f = features(:, select');
result = hypo(dt, f);

end

