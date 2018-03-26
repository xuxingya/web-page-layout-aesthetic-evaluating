#_*_ coding: utf-8 _*_
from extractor import (
  set_version,
  export,
  JpegFeature,
  TextLengthFeature,
  PictureAmountFeature,
  Normalization,
  ResizeProcessing,
  SaliencyProcessing,
  CornerProcessing,
  PixielStatistics,
  ChainOperator,
  CombineOperatorND,
  CommonStatistics,
  CommonMaxMinCountStatistics,
  MaxMinStatistics,
  StandardDeviationStatistics,
  MeanStatistics,
  DensityStatistics,
  FrameworkFeature,
  MarginFeature,
  BlockSizeFeature,
  NodeAmountFeature,
  ClusterFeature,
  )
from dataset import DataSet

set_version('exp_global')

data = DataSet('/home/gsj987/experiment/webscorer.new/groups/')
data.load_dom(5)

reload = False

def exp1():
  return JpegFeature(force_reload=reload)

def exp2():
  model0 = ResizeProcessing(0.3, 0.3, force_reload=reload)
  model1 = ChainOperator(model0, SaliencyProcessing(force_reload=reload))
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

  return CombineOperatorND(
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

def exp3():
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
  return CombineOperatorND(
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

def exp7():
  model0 = ResizeProcessing(0.3, 0.3, force_reload=reload)
  return ChainOperator(model0, FrameworkFeature(pad=1, threshold=0.00015, min_width=4,force_reload=reload))

def exp10():
  model0 = ResizeProcessing(0.3, 0.3, force_reload=reload)
  return ChainOperator(model0, MarginFeature(blocks=(33, 10, 4),force_reload=reload))

def exp4():
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

  return ChainOperator(node_features, CommonStatistics(hstack=True))

f1 = exp1()
f2 = CombineOperatorND(f1, exp2())
f3 = CombineOperatorND(f2, exp3())
f7 = CombineOperatorND(f3, exp7())
f10 = CombineOperatorND(f7, exp10())

f4 = exp4()

features = ChainOperator(f10, Normalization(0,1))


#ff4 = f4.compute(data.groups, data.labels)
ffs = features.compute(data.data, data.labels)

#import numpy as np
#fn = np.hstack((f4.get_feature_names(), features.get_feature_names()))
#final_features = np.hstack((ff4, ffs))
#print len(data.labels)
#print len(data.data)
#export({
#  'features': ffs,
#  'labels': data.labels,
#})

"""
export({
  'features': features,
  'labels': data.labels,
  'featureNames': fn,
})
"""
