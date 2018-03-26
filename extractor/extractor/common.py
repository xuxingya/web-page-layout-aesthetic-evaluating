#_*_ coding: utf-8 _*_
from feature import AbstractFeature
import numpy as np

class Normalization(AbstractFeature):
  def __init__(self, low, high, minX=None, maxX=None, dtype=np.float):
    self.low = low
    self.high = high
    self.minX = minX
    self.maxX = maxX
    self.dtype = dtype

  def _caculate(self, X):
    r = (self.maxX - self.minX)
    dx = []
    for i in range(len(X)):
      if(r[i]>0):
        dx.append((X[i]*1.0-self.minX[i]) / r[i])
      else:
        dx.append(0)
    X = np.asarray(dx)
    X = X * (self.high - self.low)
    X = X + self.low
    return X

  def compute(self, X, y):
    if self.minX is None:
      self.minX = np.min(X, axis=0)
    if self.maxX is None:
      self.maxX = np.max(X, axis=0)
    self.minX = np.asarray(self.minX)
    self.maxX = np.asarray(self.maxX)
    
    features = []
    for img in X:
      features.append(self.extract(img))
    return np.asarray(features, dtype=self.dtype)

  def extract(self, X):
    return self._caculate(X) 


class PixielStatistics(AbstractFeature):
  def __init__(self, threshold=0.5, grids=(1,1)):
    self.threshold = threshold
    self.grids = grids

  def extract(self, X):
    counts = []
    shape = X.shape
    stepX = shape[0]/self.grids[0]
    stepY = shape[1]/self.grids[1]

    for ax in range(0, shape[0], stepX):
      for ay in range(0, shape[1], stepY):
        dx = X[ax:ax+stepX, ay:ay+stepY]
        counts.append(self.do_extract(dx))
    return counts

  def do_extract(self, block_data):
    return np.sum(block_data)

  def compute(self, X, y):
    features = []
    for img in X:
      features.append(self.extract(img))
    return features

  def get_feature_names(self):
    fn = []
    for i in range(self.grids[0]):
      for j in range(self.grids[1]):
        fn.append('at(%d,%d)' %(i,j))
    return fn


class MaxMinStatistics(PixielStatistics):
  def __init__(self, max_or_min='max', *args, **kwargs):
    super(MaxMinStatistics, self).__init__(*args, **kwargs)
    self.max_or_min = 'max'

  def do_extract(self, block_data):
    if self.max_or_min == 'max':
      return np.ndarray.max(block_data)
    else:
      return np.ndarray.min(block_data)

  def get_feature_names(self):
   fn = super(MaxMinStatistics, self).get_feature_names()
   for i in range(len(fn)):
     fn[i] = self.max_or_min + ' value ' + fn[i]
   return fn


class MeanStatistics(PixielStatistics):
  def do_extract(self, block_data):
    return np.mean(block_data)

  def get_feature_names(self):
   fn = super(MeanStatistics, self).get_feature_names()
   for i in range(len(fn)):
     fn[i] = 'mean ' + fn[i]
   return fn


class StandardDeviationStatistics(PixielStatistics):
  def do_extract(self, block_data):
    return np.std(block_data)

  def get_feature_names(self):
    fn = super(StandardDeviationStatistics, self).get_feature_names()
    for i in range(len(fn)):
      fn[i] = 'sd value' + fn[i]
    return fn


class DensityStatistics(PixielStatistics):
  def __init__(self, axis=0, *args, **kwargs):
    super(DensityStatistics, self).__init__(*args, **kwargs)
    self.axis = axis

  def do_extract(self, block_data):
    shape = block_data.shape
    if self.axis==0:
      weight = np.asarray(range(shape[0]))
      sum = np.sum(np.dot(np.transpose(block_data), weight))
    else:
      weight = np.asarray(range(shape[1]))
      sum = np.sum(np.dot(block_data, weight))

    return sum*1.0/shape[self.axis]

  def get_feature_names(self):
    fn = super(DensityStatistics, self).get_feature_names()
    for i in range(len(fn)):
      fn[i] = 'density' +  str(self.axis) + ' of ' + fn[i]
    return fn


class CommonStatistics(AbstractFeature):
  resized = True
  def __init__(self, hstack=False, *args, **kwargs):
    super(CommonStatistics, self).__init__(*args, **kwargs)
    self.hstack = hstack

  def extract(self, X):
    if self.hstack:
        features = []
        CommonStatistics.resized = False
        for i in range(len(X[0])): #特征个数
          x = [f[i] for f in X]
          features += [np.max(x), np.min(x), np.mean(x), np.std(x)]
        return features
    if X: 
      return [np.max(X), np.min(X), np.mean(X), np.std(X)]
    else:
      return [0, 0, 0, 0] 

  def compute(self, X, y):
    features = []
    for x in X:
      features.append(self.extract(x))
    return features

  def get_feature_names(self):
    return ['max', 'min', 'mean', 'std']


class CommonMaxMinCountStatistics(AbstractFeature):
  resized = True
  def __init__(self, max_or_min='max', offset=0.2, hstack=False, *args, **kwargs):
    super(CommonMaxMinCountStatistics, self).__init__(*args, **kwargs)
    self.max_or_min = max_or_min
    self.offset = offset
    self.hstack = True
   
  def extract(self, X):
    if not X:
      return [0,]
    elif self.max_or_min=='max':
      m = np.max(X)
      return [len(filter(lambda x: x<m*(1-self.offset), X))]
    else:
      m = np.min(X)
      return [len(filter(lambda x: x>m*(1+self.offset), X))]
   
  def compute(self, X, y):
    features = []
    for x in X:
      features.append(self.extract(x))
    return features

  def get_feature_names(self):
    return [self.max_or_min + ' count',]
