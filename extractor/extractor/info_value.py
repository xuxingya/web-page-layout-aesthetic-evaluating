from feature import VisualFeature
from PIL import Image
from cStringIO import StringIO
import os

class JpegFeature(VisualFeature):
  def extract(self, X):
    return self.j2k_compress(X)

  def do_compute(self, X, y):
    features = []
    for img in X:
      features.append(self.j2k_compress(img))
    return features

  def j2k_compress(self, x):
    tmpOut = StringIO()
    tmpImg = Image.fromarray(x)
    tmpImg.save(tmpOut, format='jpeg')
    
    tmpOut.seek(0, os.SEEK_END)
    fileSize = tmpOut.tell()
    tmpOut.close()
    return [fileSize,]
  
  def get_feature_names(self):
    return ['JPEG map']
