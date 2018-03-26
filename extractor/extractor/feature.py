import pickle
import os
import scipy.io
import scipy.misc
import numpy as np

VERISON = 'test'
def set_version(v):
  global VERISON
  VERISON = v

def seek_path(pathname, filename):
  path = os.path.join(os.path.dirname(__file__), 'data', pathname)
  os.system('mkdir -p ' + path)
  filepath = os.path.join(path, filename)

  return filepath, os.path.isfile(filepath)


class AbstractFeature(object):
  resized = False

  def compute(self,X,y):
    raise NotImplementedError("Every AbstractFeature must implement the extract method.")

  def extract(self,X):
    raise NotImplementedError("Every AbstractFeature must implement the extract method.")

  def save(self):
    raise NotImplementedError("Every AbstractFeature must implement the extract method.")
   
  def load(self):
    raise NotImplementedError("Every AbstractFeature must implement the extract method.")
  
  def __repr__(self):
    return "AbstractFeature"

  def get_feature_names(self):
    return []

  def get_labels(self, data):
    if data.groups:
      return data.node_labels()
    else:
      return data.labels

class VisualFeature(AbstractFeature):

  def __init__(self, force_reload=False):
    self.force_reload = force_reload
    self.save_count = 0

  def compute(self,X,y):
    data_loaded = self.load()
    if (not data_loaded) or self.force_reload:
      self.features = self.do_compute(X, y)
      self.save()
    return self.features
  
  def do_compute(self, X, y): 
    raise NotImplementedError("Every AbstractFeature must implement the extract method.")

  def dump_to_save(self): 
    return {
      'features': self.features
    }

  def load_data(self, data): 
    self.features = data['features']

  def name_to_save(self):
    return self.__class__.__name__

  def save(self):
    path, found = seek_path(self.name_to_save(), VERISON)
    if (not found) or self.force_reload:
      outfile = open(path, 'wb')
      pickle.dump(self.dump_to_save(), outfile, protocol=pickle.HIGHEST_PROTOCOL)
      outfile.close()
 
  def load(self):
    path, found = seek_path(self.__class__.__name__, VERISON)
    if found and (not self.force_reload):
      infile = open(path, 'rb')
      data = pickle.load(infile)
      infile.close()
      self.load_data(data)
      return True
    return False

  def get_feature_names(self): 
    raise NotImplementedError("Every VisualFeature must implement the get feature names method.")

  def save_img(self, X):
    p = os.path.join(os.path.dirname(__file__), 'img', self.__class__.__name__, VERISON)
    os.system('mkdir -p '+p)

    scipy.misc.imsave(os.path.join(p, '%d.jpg' %self.save_count) , np.array(X))
    self.save_count += 1
    


class NodeFeature(VisualFeature):
  def get_feature_names(self): 
    raise NotImplementedError("Every NodeFeature must implement the get feature names method.")


class Identity(AbstractFeature):
  """
  Simplest AbstractFeature you could imagine. It only forwards the data and does not operate on it, 
  probably useful for learning a Support Vector Machine on raw data for example!
  """
  def __init__(self):
    AbstractFeature.__init__(self)
    
  def compute(self,X,y):
    return X
  
  def extract(self,X):
    return X
  
  def __repr__(self):
    return "Identity"


def export(to_export):
  path = os.path.join('..', 'exports', VERISON+'.mat')
  scipy.io.savemat(path, mdict=to_export)
