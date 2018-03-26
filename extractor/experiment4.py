#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  Normalization,
  CombineOperatorND,
  ChainOperator,
  TextLengthFeature,
  BlockSizeFeature,
  PictureAmountFeature,
  NodeAmountFeature,
  ClusterFeature,
  CommonStatistics,
  )
from dataset import DataSet

set_version('exp4')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
data.load_dom(5)

reload = True

model0 = TextLengthFeature(force_reload=reload)
model1 = PictureAmountFeature(force_reload=reload)
model2 = BlockSizeFeature(force_reload=reload)
model3 = NodeAmountFeature(force_reload=reload)
model4 = TextLengthFeature(force_reload=reload, per_depth=True)
model5 = NodeAmountFeature(force_reload=reload, per_depth=True)

node_features = ClusterFeature(
  CombineOperatorND(model0, 
    CombineOperatorND(model1, 
      CombineOperatorND(model2, 
        CombineOperatorND(model3, 
          CombineOperatorND(model4, model5))))),
  combine=False,
  force_reload=reload 
  )

model6 = ChainOperator(node_features, CommonStatistics(hstack=True))
features = ChainOperator(model6, Normalization(0,1))


export({
  'features': features.compute(data.groups, data.labels),
  'labels': features.get_labels(data),
  'featureNames': features.get_feature_names(),
})

d = 0
for i, g in enumerate(data.groups):
  c = 0
  for n in g.nodes:
    if n['sitename'] == 'wordreference_com' and c in node_features.index[i]:
        print d+node_features.index[i].index(c), n['nodeName'], n['nodeText'], n['pos']
    c += 1
  d += len(node_features.index[i])
