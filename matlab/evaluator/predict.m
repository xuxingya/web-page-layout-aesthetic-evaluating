function [allscores,scores0,scores1] = predict( xp,yp,theta )
%xp,yp for predict not for train
m = size(xp,1);
% p = zeros(m,1);%the predict output --fenlei jieguo 
% for k = 1 : m
%     p(k) = hypo(theta, xp(k, :));
% end
p = hypo(theta, xp);
p(p>=0.5) = 1;
p(p<0.5) = 0;
allscores = sum(yp==p)/m;
scores0 = sum(yp(yp==0)==p(yp==0))/length(yp(yp==0));
scores1 = sum(yp(yp==1)==p(yp==1))/length(yp(yp==1));
end

