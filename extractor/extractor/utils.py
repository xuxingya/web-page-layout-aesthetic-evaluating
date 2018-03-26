def cssText(css):
  return dict(filter(lambda x: len(x)==2, map(lambda x: map(lambda y:y.strip(), x.split(': ')), css.split(';'))[:-1]))

def compaireByKey(d1, d2, weights): 
  mid = ["bottom", "top", "left", "right"]
  right = ["width", "color", "style"]
  default = {
    'radius': '0px',
    'width': '0px',
    'style': 'none',
    'color': 'rgb(0, 0, 0)',
  }

  dom1  = cssText(d1["nodeStyle"]["cssText"])
  dom2  = cssText(d2['nodeStyle']['cssText'])

  bs = 0
  for m in mid:
    for r in right:
      attr = "border-"+m+"-"+r
      if dom1[attr] == dom2[attr] and dom1[attr]!=default[r]:
        bs += weights['border']
  for mf in mid[:2]:
    for mb in mid[2:]:
      attr = "border-%s-%s-radius" %(mf, mb)
      if dom1[attr] == dom2[attr] and dom1[attr]!=default['radius']:
        bs += weights['border']

  for m in mid:
    for _attr in ["margin", "padding"]:
      attr = _attr + '-' + m
      if dom1[attr]==dom2[attr] and dom1[attr]!='1px':
        bs += weights[_attr]

  for attr in ('width', 'height'):
    if dom1[attr]==dom2[attr]:
      bs += weights[attr]

  if dom1['width'] == dom2['width'] and dom1['height'] == dom2['height']:
    bs += weights['width_and_height']

  if dom1['font-size'] == dom2['font-size']:
    bs += weights['fontSize']

  return bs
