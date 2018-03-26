from feature import VisualFeature
import numpy as np
import cv2

class FrameworkFeature(VisualFeature):
  def __init__(self, pad=1, threshold=0.0001, min_width=3, *args, **kwargs):
    self.pad = pad
    self.threshold = threshold
    self.min_width = min_width
    super(FrameworkFeature, self).__init__(*args, **kwargs)

  def extract(self, X):
    dX = cv2.Canny(X, 20, 50)
    self.h, self.w = dX.shape

    H = self.build_diff(np.sum(dX, axis=0))
    V = self.build_diff(np.sum(dX, axis=1))
    self.save_img(H)
    self.save_img(V)
 
    features = []
    labels = []
   
    p = []
    for X, l in ((H, 'H'), (V, 'V')):
      self.l = (self.pad, l)
      self.build_cluster(X, self.pad)
      self.maxmin_width(features, labels)
      self.symmetry_analsys(X, features, labels)
      self.count_analsys(features, labels)
      self.width_analsys(features, labels)
      self.pulse_anasys(features, labels)
      p.append(self.pulse)
    self.compare(p[0], p[1], features, labels)

    #for i in range(len(features)):
    #  print labels[i], ':', features[i]
    self.labels = labels
    return  features

  def maxmin_width(self, features, labels):
    if self.arrange.keys():
      max_width = np.max(self.arrange.keys())
      min_width = np.min(self.arrange.keys())
    else:
      max_width = 0
      min_width = 0

    for mw, l in ((max_width,'max'), (min_width, 'min'),):
      labels.append('width of %s cluster of %s %d' %(l, self.l[1], self.l[0]))
      features.append(mw)

      labels.append('count of %s cluster of %s %d' %(l, self.l[1], self.l[0]))
      features.append(self.arrange.get(mw, {'count':0})['count'])

  def symmetry_analsys(self, X, features, labels):
    sum = []
    for width in self.arrange.keys():
      left = self.arrange[width]['edges'][0][0]
      right = self.arrange[width]['edges'][-1][1]
      _s = 0
      for i in range(left, right+1):
        _s += abs(X[i]-X[right-(i-left)])
      sum.append(1.0/_s)
    self._analysis(features, labels, 'symmetry', sum)    
    
  def count_analsys(self, features, labels):
    count = [c['count'] for c in self.arrange.values()]
    self._analysis(features, labels, 'count', count)

  def width_analsys(self, features, labels):
    width = self.arrange.keys()
    self._analysis(features, labels, 'width', width)

  def pulse_anasys(self, features, labels):
    self._analysis(features, labels, 'pulse', self.pulse)
    if not self.pulse:
      maxh = 0
      minh = 0
    else:
      maxh = np.max(self.pulse)
      minh = np.min(self.pulse)
    labels.append('count of high pulse of %s %d' %(self.l[1], self.l[0]))
    features.append(len(filter(lambda x: x>maxh*0.8, self.pulse)))
    
    labels.append('count of low pulse of %s %d' %(self.l[1], self.l[0]))
    features.append(len(filter(lambda x: x<minh*1.2, self.pulse)))

  def compare(self, hpulse, vpulse, features, labels):
    labels.append('compare of H and V count of %d' %self.l[0])
    if len(vpulse):
      features.append(len(hpulse)*1.0/len(vpulse))
    else:
      features.append(0)

  def _analysis(self, features, labels, name, value):
    labels.append('max %s of %s %d' %(name, self.l[1], self.l[0]))
    features.append(np.max(value) if value else 0)

    labels.append('min %s of %s %d' %(name, self.l[1], self.l[0]))
    features.append(np.min(value) if value else 0)

    labels.append('std %s of %s %d' %(name, self.l[1], self.l[0]))
    features.append(np.std(value) if value else 0)

    labels.append('mean %s of %s %d' %(name, self.l[1], self.l[0]))
    features.append(np.mean(value) if value else 0)


  def build_cluster(self, X, pad):
    self.arrange = {}
    self.pulse = []
    self.position = []
    for i, x in enumerate(X):
      h = x * pad
      if h > 0:
        self.pulse.append(h)
        for j in self.position:
          width = i-j
          if width >= self.min_width:
            if width in self.arrange:
              if self.arrange[width]['edges'][-1][1] < j:
                self.arrange[width]['count'] += 1
                self.arrange[width]['edges'].append((j,i))
            else:
              self.arrange[width] = {
                'count': 1,
                'edges': [(j,i),]
              }
        self.position.append(i)
    
    for w in self.arrange.keys():
      if self.arrange[w]['count'] == 1:
        self.arrange.pop(w)

  def build_diff(self, X):
    width = X.shape[0]
    fixed = int(1263.0/1280*self.w)
    if width ==self.w:
      width = fixed 
    wh = {
      fixed: self.h,
      self.h: fixed
    }
    _m = np.max(X)
    dX = []
    for i in range(width-1):
      dX.append((X[i+1]*1.0/_m)-(X[i]*1.0/_m))
    hX = []
    for i,x in enumerate(dX):
      dx = x
      if np.abs(x)*1.0/wh[width]<self.threshold:
        hX.append(0)
      else:
        hX.append(dx)
    return hX

  def save_img(self, X):
    height = 300
    width = len(X)
    img = np.zeros(( height, width))

    min = np.min(X)
    max = np.max(X) - min

    for i,h in enumerate(X):
      h = (h*1.0-min)/max
      for j in range(300-int(h*300), 300):
        img[j,i] = 255
    super(FrameworkFeature, self).save_img(img)    

  def do_compute(self, X, y):
    features = []
    for x in X:
      features.append(self.extract(x))
    return features

  def get_feature_names(self):
    return self.labels


if __name__ == '__main__':  
  import cv2
  img = cv2.imread('/home/gsj987/experiment/webscorer.new/groups/bad/bitauto_com_g.png', 0)
  ff = FrameworkFeature(threshold=0,force_reload=True)
  print ff.extract(img)
