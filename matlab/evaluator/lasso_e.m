sel = 1:0.3:4;

sc = []

for i=1:length(sel)
    select = abs(theta)>sel(i);
    sc = [sc sum(select)];
end

sc