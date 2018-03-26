#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  ResizeProcessing,
  FrameworkFeature,
  Normalization,
  ChainOperator,
  )
from dataset import DataSet

set_version('exp7')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')

model0 = ResizeProcessing(0.3, 0.3, force_reload=True)
model1 = ChainOperator(model0, FrameworkFeature(pad=1, threshold=0.00015, min_width=4,force_reload=True))

o_features = model1

features = ChainOperator(o_features, Normalization(0,1))


export({
  'features': features.compute(data.data, data.labels),
  'labels': data.labels,
  'featureNames': features.get_feature_names(),
})
