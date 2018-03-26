#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  Normalization,
  CombineOperatorND,
  ChainOperator,
  TextLengthFeature,
  PictureAmountFeature,
  ResizeProcessing,
  SaliencyProcessing,
  PixielStatistics,
  MaxMinStatistics,
  StandardDeviationStatistics,
  DensityStatistics,
  NodeAmountFeature,
  ClusterFeature,
  BlockSizeFeature,
  ComplexNodeFeature,
  )
from dataset import DataSet

set_version('exp5')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
data.load_dom(5, (4,4))

for group in data.groups:
  for node in group.nodes:
    t,l,w,h = node['pos']
    if (w==0) or (h==0):
      print t,l,w,h


reload = True

model0 = ResizeProcessing(0.3, 0.3, force_reload=reload)
model1 = ChainOperator(model0, SaliencyProcessing(force_reload=reload))
model2 = ChainOperator(model1, PixielStatistics(threshold=0.1, grids=(1,1)))
model3 = ChainOperator(model1, MaxMinStatistics(max_or_min="max", threshold=0.1, grids=(1,1)))
model4 = ChainOperator(model1, MaxMinStatistics(max_or_min="min", threshold=0.1, grids=(1,1)))
model5 = ChainOperator(model1, StandardDeviationStatistics(threshold=0.1, grids=(1,1)))
model8 = ChainOperator(model1, DensityStatistics(axis=0, threshold=0.1, grids=(1,1)))
model9 = ChainOperator(model1, DensityStatistics(axis=1, threshold=0.1, grids=(1,1)))

img_features = CombineOperatorND(
  CombineOperatorND(
      CombineOperatorND(
        CombineOperatorND(
          CombineOperatorND(model2, model3), 
          model4), 
        model5),
    model8),
  model9)

model10 = TextLengthFeature(force_reload=reload)
model11 = PictureAmountFeature(force_reload=reload)
model12 = BlockSizeFeature(force_reload=reload)
model13 = NodeAmountFeature(force_reload=reload)
model14 = TextLengthFeature(force_reload=reload, per_depth=True)
model15 = NodeAmountFeature(force_reload=reload, per_depth=True)

node_features = ClusterFeature(
  CombineOperatorND(model10, 
    CombineOperatorND(model11, 
      CombineOperatorND(model12, 
        CombineOperatorND(model13, 
          CombineOperatorND(model14, model15))))),
  force_reload=reload 
  )


combined_features = ComplexNodeFeature(node_model=node_features, img_model=img_features)
features = ChainOperator(combined_features, Normalization(0,1))



export({
  'features': features.compute(data.groups, data.labels),
  'labels': features.get_labels(data),
  'featureNames': features.get_feature_names(),
})
