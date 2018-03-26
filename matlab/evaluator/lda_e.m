labels(labels==2)=1;

W = LDA(PCAFeatures, labels);
L = [ones(length(PCAFeatures),1) PCAFeatures] * W';