dataNum = '7';
load(['data/exp' dataNum '.mat']);
good=features(labels==2,:);
bad=features(labels==0,:);
gl=length(good(:,1));
bl=length(bad(:,1));
f=70;   %分割的趟数

for i = 1 : length(features(1,:))
    s=min(features(:,1));
    t=max(features(:,1));
    figure;
    gp=zeros(f);
    bp=zeros(f);
    x=zeros(f);
    for j = 1:gl
        gp( fix(good(j,i)/((t-s)/(f-2))) +1 ) = gp( fix(good(j,i)/((t-s)/(f-2))) +1 ) + 1;
    end
    for j = 1:bl
        bp(fix(bad(j,i)/((t-s)/(f-2))) +1 ) = bp(fix(bad(j,i)/((t-s)/(f-2))) +1 ) +1;
    end
    for j = 1:f-1
        x(j)=s+(j-1)*(t-s)/(f-2);
        gp(j+1)=gp(j+1)+gp(j);
        bp(j+1)=bp(j+1)+bp(j);
    end
    gp=gp/gl;
    bp=bp/bl;
    hold on;
    H1 = plot(x,gp,'b');%好值的图
    H2 = plot(x,bp,'r');%坏值的图
    hold off;
    h = get(gca,'Children');
    v = [h(f+1),h(1)];
    legend(v, 'good', 'bad');
    title(featureNames(i,:));
    ylabel('probability');
    
    saveas(gcf, ['cdf/exp' dataNum '/' num2str(i) '_' featureNames(i,:)], 'png'); 
    close;
    %plot(x,gp-bp,'g');%上行差异值（峰值倾向于出现在小的地方）
    %plot(x,abs(gp-bp),'k');%绝对峰值
end
