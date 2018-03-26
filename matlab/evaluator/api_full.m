function result = api_full( args )
%API Summary of this function goes here
%   Detailed explanation goes here

features = args.feature;
load dt.117.full.mat;

f = features;
result = hypo(dt, f);

end

