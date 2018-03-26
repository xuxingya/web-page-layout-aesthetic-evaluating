#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  ResizeProcessing,
  MarginFeature,
  Normalization,
  ChainOperator,
  CombineOperatorND,
  TextLengthFeature,
  PictureAmountFeature,
  NodeAmountFeature,
  ClusterFeature,
  BlockSizeFeature,
  ComplexNodeFeature,
  )
from dataset import DataSet

set_version('exp11')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
data.load_dom(5, (4,4))

reload = True

model0 = ResizeProcessing(0.3, 0.3, force_reload=reload)
model1 = ChainOperator(model0, MarginFeature(force_reload=reload))
model2 = ChainOperator(model0, MarginFeature(absolute=False, force_reload=reload))

img_features = CombineOperatorND(model1, model2)

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
