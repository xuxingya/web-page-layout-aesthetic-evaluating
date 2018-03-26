function [ val ] = regular( theta )
tmp1=theta(abs(theta)>0.2);
tmp2=theta(abs(theta)<=0.2);
val = sum(5*tmp2.^2)+sum(abs(tmp1));
end

