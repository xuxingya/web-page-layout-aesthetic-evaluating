function l = likehood(theta, xl, yl)
    l = sum(yl.*log(hypo(theta,xl))+(1-yl).*log(1.-hypo(theta,xl)));
%     for i=1:size(xl,1)
%         l = l + yl(i)*log(hypo(theta, xl(i,:)))+(1-yl(i))*log(1-hypo(theta, xl(i,:)));
%     end
end
