from feature import VisualFeature
from libs.blank import BlankArea
import numpy as np


class MarginFeature(VisualFeature):
  def __init__(self, blocks, threshold=5, *args, **kwargs):
    super(MarginFeature, self).__init__(*args, **kwargs)
    self.block_sizes = blocks
    self.threshold = threshold
    self.colors = ((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,255,255))

  def extract(self, X):
    global c
    ba = BlankArea(X)
    features = []
    for i, bs in enumerate(self.block_sizes):
      ba.scanImg((bs,bs), color=self.colors[i], thershold=self.threshold)
      ai = np.sum(ba.getTemporaryImage())
      contours, roi = ba.getContours()
      print roi
      if contours:
        dx = []
        dy = []
        r = []
        for j, c in enumerate(contours):
          if c== bs*bs:
            continue
          mx = roi[j][0] + roi[j][2]*1.0/2
          my = roi[j][1] + roi[j][3]*1.0/2
          dx.append( mx*c)
          dy.append(my*c)
          r.append(roi[j][2]*roi[j][3]*1.0/c)
        contours = filter(lambda x: x>bs*bs, contours)
        if contours: 
          features+= [ai, np.max(contours), np.min(contours), np.mean(contours), np.std(contours), len(contours), np.mean(dx), np.mean(dy), np.mean(r)]
        else:
          features += [ai, 0, 0, 0, 0, 0, 0, 0, 0]
      else:
        features+= [ai, 0, 0, 0, 0, 0, 0, 0, 0]
      print contours

    self.save_img(ba.outputImg)
    return features

  def do_compute(self, X, y):
    features = []
    for img in X:
      features.append(self.extract(img))
    return features

  def get_feature_names(self):
    names = []
    labels = ['area', 'max', 'min', 'mean', 'std', 'count', 'dx', 'dy', 'r']
    for i in self.block_sizes:
      for j in range(len(labels)):
        names.append(labels[j] + ' of margin with ' + str(i))
    return names
