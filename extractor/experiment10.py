#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  ResizeProcessing,
  MarginFeature,
  Normalization,
  ChainOperator,
  )
from dataset import DataSet

set_version('exp10')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')

model0 = ResizeProcessing(0.3, 0.3, force_reload=True)
model1 = ChainOperator(model0, MarginFeature(blocks=(33, 10, 4),force_reload=True))

o_features = model1

features = ChainOperator(o_features, Normalization(0,1))

print features.get_feature_names()

export({
  'features': features.compute(data.data, data.labels),
  'labels': data.labels,
  'featureNames': features.get_feature_names(),
})
