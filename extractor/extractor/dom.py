from feature import NodeFeature
from utils import compaireByKey
import numpy as np

class TextLengthFeature(NodeFeature):
  def __init__(self, per_depth=False, *args, **kwargs):
    super(TextLengthFeature, self).__init__(*args, **kwargs)
    self.per_depth = per_depth

  def extract(self, X):
    features = []
    for node in X.nodes:
      text = node['nodeText']
      text_length = len(text) if text else 0
      if self.per_depth:
        text_length = text_length*1.0 / (1+X.max_depth-node['depth'])
      features.append([text_length,])
    return features

  def do_compute(self, groups, y):
    features = []
    for group in groups:
      features += self.extract(group)
    return features

  def get_feature_names(self):
    if not self.per_depth:
      return ['text length']
    else:
      return ['text length per depth']

  def name_to_save(self):
    name = super(TextLengthFeature, self).name_to_save()
    if self.per_depth:
      return 'per_'+name
    else:
      return name


class PictureAmountFeature(NodeFeature):
  def extract(self, group):
    features = []
    mapping = group.get_mapping()

    count = {}
    def plus(id):
      id = int(id)
      if id not in count:
        count[id] = 1
      else:
        count[id] += 1

    for node in group.nodes:
      bg = filter(lambda x: x.startswith(' background-image'), node['nodeStyle']['cssText'].split(';'))
      if node['nodeName'].lower() == 'img' or (bg and not bg[0].endswith('none')):
        cn = node
        plus(cn['id'])
        while cn and cn['parentId']:   
          plus(cn['parentId'])
          cn = mapping.get(int(cn['parentId']), None)

    for node in group.nodes:
      features.append([count.get(int(node['id']), 0), ]) 

    return features

  def do_compute(self, groups, y):
    features = []
    for group in groups:
      features += self.extract(group)
    return features

  def get_feature_names(self):
    return ['picture count']


class BlockSizeFeature(NodeFeature):
  def extract(self, group):
    features = []
    for node in group.nodes:
      t, l, w, h = node['pos']
      d = node['depth']
      features.append([w, h, t, l, d])
    return features

  def do_compute(self, groups, y):
    features = []
    for group in groups:
      features += self.extract(group)
    return features

  def get_feature_names(self):
    return ['width', 'height', 'top', 'left', 'depth']


class NodeAmountFeature(NodeFeature):
  def __init__(self, per_depth=False, *args, **kwargs):
    super(NodeAmountFeature, self).__init__(*args, **kwargs)
    self.per_depth = per_depth

  def extract(self, group):
    features = []
    mapping = group.get_mapping()

    count = {}
    def plus(id):
      id = int(id)
      if id not in count:
        count[id] = 1
      else:
        count[id] += 1

    for node in group.nodes:
      cn = node
      plus(cn['id'])
      while cn and cn['parentId']:   
        plus(cn['parentId'])
        cn = mapping.get(int(cn['parentId']), None)

    for node in group.nodes:
      length = count.get(int(node['id']), 0)
      if self.per_depth:
        length = length * 1.0 / (1+group.max_depth - node['depth'])
      features.append([ length, ]) 

    return features

  def do_compute(self, groups, y):
    features = []
    for group in groups:
      features += self.extract(group)
    return features

  def get_feature_names(self):
    if not self.per_depth:
      return ['node count']
    else:
      return ['node count per depth']

  def name_to_save(self):
    name = super(NodeAmountFeature, self).name_to_save()
    if self.per_depth:
      return 'per_'+name
    else:
      return name

class ClusterFeature(NodeFeature):
  def __init__(self, model, k=8, weights={}, combine=True, *args, **kwargs):
    super(ClusterFeature, self).__init__(*args, **kwargs)
    self.model = model
    self.k = k
    self.index = []
    self.weights = {
      'fontSize': 2,
      'width': 2,
      'height': 3,
      'padding': 0.5,
      'margin': 0.5,
      'border': 1,
      'width_and_height': 4,
    }
    self.weights.update(weights)
    self.combine = combine

  def dump_to_save(self):
    to_save = super(ClusterFeature, self).dump_to_save()
    to_save.update({
      'index': self.index,
    })
    return to_save

  def load_data(self, data):
    super(ClusterFeature, self).load_data(data)
    self.index = data['index']

  def extract(self, group):
    features = []
    parents = {}
    self.extracted_index = []
    for i, node in enumerate(group.nodes):
      if node['parentId']:
        if node['parentId'] in parents:
          parents[node['parentId']].append(i)
        else:
          parents[node['parentId']] = [i,]
      else:
        self.extracted_index.append(i)
        features.append(1) #one count
    
    for parent in parents.values():
      samples = []
      counts = []
      for id in parent:
        node = group.nodes[id]
        find_cluster = False
        for i, sample_id in enumerate(samples):
          sample = group.nodes[sample_id]
          score = compaireByKey(node, sample, self.weights)
          if score > self.k:
            counts[i] += 1
            find_cluster = True
            break
        if not find_cluster:
           samples.append(id)
           counts.append(1)
    
      self.extracted_index += samples
      features += counts

    origin_features  = self.model.extract(group) 
    combiled_features = []

    for i, id in enumerate(self.extracted_index):
      f = origin_features[id]
      f = np.hstack((f, [features[i]]))
      combiled_features.append(f)

    return combiled_features

  def do_compute(self, groups, y):
    features = []
    self.index = []
    for group in groups:
      if self.combine:
        features += self.extract(group)
        self.index.append( self.extracted_index )
      else:
        features.append(self.extract(group))
        self.index.append([0])
    return features

  def get_feature_names(self):
    ofn = self.model.get_feature_names()
    ofn.append('cluster count')
    return ofn

  def get_labels(self, data):
    labels = data.labels
    new_labels = []
    for i, index in enumerate(self.index):
      new_labels += ([labels[i]] * len(index))
    return new_labels
