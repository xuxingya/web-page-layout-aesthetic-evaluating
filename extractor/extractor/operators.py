from feature import AbstractFeature
from dom import ClusterFeature
import numpy as np

class FeatureOperator(AbstractFeature):
  """
  A FeatureOperator operates on two feature models.
  
  Args:
    model1 [AbstractFeature]
    model2 [AbstractFeature]
  """
  def __init__(self,model1,model2):
    if (not isinstance(model1,AbstractFeature)) or (not isinstance(model2,AbstractFeature)):
      raise Exception("A FeatureOperator only works on classes implementing an AbstractFeature!")
    self.model1 = model1
    self.model2 = model2
  
  def __repr__(self):
    return "FeatureOperator(" + repr(self.model1) + "," + repr(self.model2) + ")"
  
class ChainOperator(FeatureOperator):
  """
  The ChainOperator chains two feature extraction modules:
    model2.compute(model1.compute(X,y),y)
  Where X can be generic input data.
  
  Args:
    model1 [AbstractFeature]
    model2 [AbstractFeature]
  """
  def __init__(self,model1,model2):
    FeatureOperator.__init__(self,model1,model2)
    
  def compute(self,X,y):
    X = self.model1.compute(X,y)
    return self.model2.compute(X,y)
    
  def extract(self,X):
    X = self.model1.extract(X)
    return self.model2.extract(X)
  
  def __repr__(self):
    return "ChainOperator(" + repr(self.model1) + "," + repr(self.model2) + ")"
 
  def get_feature_names(self):
    fn1 = self.model1.get_feature_names()
    fn2 = self.model2.get_feature_names()
    fn = []
    if not fn1:
      return fn2
    if not fn2 or self.model1.resized:
      return fn1
    if self.model2.resized:
      for f2 in fn2:
        fn.append(fn1[0]+' '+f2)
    else: 
      for f1 in fn1:
        for f2 in fn2:
          fn.append(f1+' '+f2)
    return fn

  def get_labels(self, data):
    label1 = self.model1.get_labels(data)
    label2 = self.model2.get_labels(data)
    if len(label1) > len(label2):
      return label2
    else:
      return label1

class CombineOperator(FeatureOperator):
  """
  The CombineOperator combines the output of two feature extraction modules as:
    (model1.compute(X,y),model2.compute(X,y))
  , where the output of each feature is a [1xN] or [Nx1] feature vector.
    
    
  Args:
    model1 [AbstractFeature]
    model2 [AbstractFeature]
    
  """
  def __init__(self,model1,model2):
    FeatureOperator.__init__(self, model1, model2)
    
  def compute(self,X,y):
    A = self.model1.compute(X,y)
    B = self.model2.compute(X,y)
    C = []
    for i in range(0, len(A)):
      ai = np.asarray(A[i]).reshape(1,-1)
      bi = np.asarray(B[i]).reshape(1,-1)
      C.append(np.hstack((ai,bi)))
    return C
  
  def extract(self,X):
    ai = self.model1.extract(X)
    bi = self.model2.extract(X)
    ai = np.asarray(ai).reshape(1,-1)
    bi = np.asarray(bi).reshape(1,-1)
    return np.hstack((ai,bi))

  def __repr__(self):
    return "CombineOperator(" + repr(self.model1) + "," + repr(self.model2) + ")"
   
  
  def get_feature_names(self):
    fn1 = self.model1.get_feature_names()
    fn2 = self.model2.get_feature_names()

    return list(fn1) + list(fn2)


class CombineOperatorND(FeatureOperator):
  """
  The CombineOperator combines the output of two multidimensional feature extraction modules.
    (model1.compute(X,y),model2.compute(X,y))
    
  Args:
    model1 [AbstractFeature]
    model2 [AbstractFeature]
    hstack [bool] stacks data horizontally if True and vertically if False
    
  """
  def __init__(self,model1,model2, hstack=True):
    FeatureOperator.__init__(self, model1, model2)
    self._hstack = hstack
    
  def compute(self,X,y):
    A = self.model1.compute(X,y)
    B = self.model2.compute(X,y)
    C = []
    for i in range(0, len(A)):
      if self._hstack:
        C.append(np.hstack((A[i],B[i])))
      else:
        C.append(np.vstack((A[i],B[i])))
    return C
  
  def extract(self,X):
    ai = self.model1.extract(X)
    bi = self.model2.extract(X)
    if self._hstack:
      return np.hstack((ai,bi))
    return np.vstack((ai,bi))

  def __repr__(self):
    return "CombineOperatorND(" + repr(self.model1) + "," + repr(self.model2) + ", hstack=" + str(self._hstack) + ")"

  def get_feature_names(self):
    fn1 = self.model1.get_feature_names()
    fn2 = self.model2.get_feature_names()

    return fn1 + fn2


class ComplexNodeFeature(AbstractFeature):
  def __init__(self, img_model, node_model, *args, **kwargs):
    super(ComplexNodeFeature, self).__init__(*args, **kwargs)
    if not isinstance(img_model, AbstractFeature):
      raise Exception('img model must be instance of AbstractFeature')
    self.img_model = img_model
    self.node_model = node_model

  def extract(self, X):
    # X should be dataset
    ai = self.node_model.extract(X)
    img_data = X.all_img_data()
    if isinstance(self.node_model, ClusterFeature):
      img_data = [img_data[i] for i in self.node_model.extracted_index]
    bi = self.img_model.extract(img_data)
    ci = []
    for i in range(len(ai)):
      ci.append(np.hstack((ai[i], bi[i]))) 
    return ci

  def compute(self, X, y=None):
    # X is groups, y is labels
    A = self.node_model.compute(X, y)
    B = []
    for j, g in enumerate(X):
      img_data = g.all_img_data()
      if isinstance(self.node_model, ClusterFeature):
        img_data = [img_data[i] for i in self.node_model.index[j]]
      B += self.img_model.compute(img_data, y)
    C = []
    for i in range(len(A)):
      C.append(np.hstack((A[i], B[i])))
    return C

  def get_feature_names(self):
    fn1 = self.node_model.get_feature_names()
    fn2 = self.img_model.get_feature_names()

    return fn1 + fn2

  def get_labels(self, data):
    return self.node_model.get_labels(data)
