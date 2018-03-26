from feature import VisualFeature
from libs.saliency.saliency_map import SaliencyMap
import cv2
import numpy as np

class Preprocessing(VisualFeature):
  def do_compute(self, X, y):
    features = []
    for img in X:
      sm = self.extract(img)
      features.append(sm)
    return features

class SaliencyProcessing(Preprocessing):
  def extract(self, X):
    bgr = cv2.cvtColor(X, cv2.COLOR_GRAY2BGR)
    sm = SaliencyMap(bgr)
    self.save_img(sm.map)
    return sm.map

  def get_feature_names(self):
    return ['saliency map']

class CornerProcessing(Preprocessing):
  def __init__(self, 
    minV=10, 
    maxV=200, 
    blockSize=2, 
    ksize=3, 
    k=0.04, *args, **kwargs):
    super(CornerProcessing, self).__init__(*args, **kwargs)
    self.minV = minV
    self.maxV = maxV
    self.blockSize = blockSize
    self.ksize = ksize
    self.k = k

  def extract(self, X):
    ims = cv2.Canny(X, self.minV, self.maxV)
    im = cv2.cornerHarris(ims, self.blockSize, self.ksize, self.k)
    self.save_img(im)
    return im

  def get_feature_names(self):
    return ['corner map']

class ResizeProcessing(Preprocessing):
  def __init__(self, fx=0.5, fy=0.5, *args, **kwargs):
    super(ResizeProcessing, self).__init__(*args, **kwargs)
    self.fx = fx
    self.fy = fy

  def extract(self, X):
    dx = cv2.resize(X, (0,0), fx=self.fx, fy=self.fy)
    return dx

  def get_feature_names(self):
    return ['resized']
