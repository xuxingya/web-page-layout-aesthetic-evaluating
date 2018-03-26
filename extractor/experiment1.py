#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  JpegFeature,
  TextLengthFeature,
  PictureAmountFeature,
  Normalization,
  ChainOperator,
  CombineOperatorND,
  ComplexNodeFeature,
  )
from dataset import DataSet

set_version('exp1')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
data.load_dom(0)

reload = True


model0 = TextLengthFeature(force_reload=reload)
model1 = CombineOperatorND(model0, PictureAmountFeature(force_reload=reload))

img_model = JpegFeature(force_reload=reload)
node_features = ComplexNodeFeature(node_model=model1, img_model=img_model)

features = ChainOperator(node_features, Normalization(0,1))

export({
  'features': features.compute(data.groups, data.labels),
  'labels': data.node_labels(),
  'featureNames': features.get_feature_names(),
})
