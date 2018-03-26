#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  ResizeProcessing,
  CornerProcessing,
  PixielStatistics,
  Normalization,
  ChainOperator,
  CombineOperatorND,
  CommonMaxMinCountStatistics,
  CommonStatistics,
  MaxMinStatistics,
  StandardDeviationStatistics,
  MeanStatistics,
  DensityStatistics,
  )
from dataset import DataSet

set_version('exp3')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
reload = True

model0 = ResizeProcessing(0.3, 0.3)
model1 = ChainOperator(model0, CornerProcessing())
model2 = ChainOperator(model1, PixielStatistics(threshold=0.1, grids=(3,4)))
model3 = ChainOperator(model1, MaxMinStatistics(max_or_min="max", threshold=0.1, grids=(3,4)))
model4 = ChainOperator(model1, MaxMinStatistics(max_or_min="min", threshold=0.1, grids=(3,4)))
model5 = ChainOperator(model1, StandardDeviationStatistics(threshold=0.1, grids=(3,4)))
model6 = ChainOperator(model1, StandardDeviationStatistics(threshold=0.1, grids=(1,1)))
model7 = ChainOperator(model1, MeanStatistics(threshold=0.1, grids=(1,1)))
model8 = ChainOperator(model1, DensityStatistics(axis=0, threshold=0.1, grids=(1,1)))
model9 = ChainOperator(model1, DensityStatistics(axis=1, threshold=0.1, grids=(1,1)))

model10 = ChainOperator(model2, CommonStatistics())
model11 = ChainOperator(model3, CommonStatistics())
model12 = ChainOperator(model4, CommonStatistics())
model13 = ChainOperator(model5, CommonStatistics())
model14 = ChainOperator(model2, CommonMaxMinCountStatistics('max'))
model15 = ChainOperator(model2, CommonMaxMinCountStatistics('min'))


o_features = \
  CombineOperatorND(
    CombineOperatorND(
      CombineOperatorND(
        CombineOperatorND(
          CombineOperatorND(
            CombineOperatorND(
              CombineOperatorND(
                CombineOperatorND(
                  CombineOperatorND(model14, model15),
                  model10), 
              model11),
            model12), 
          model13), 
        model6),
      model7),
    model8),
  model9)

features = ChainOperator(o_features, Normalization(0,1))

export({
  'features': features.compute(data.data, data.labels),
  'labels': data.labels,
  'featureNames': features.get_feature_names(),
})
