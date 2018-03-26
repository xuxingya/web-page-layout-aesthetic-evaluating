import json

def decode(obj, depth=4):
  if isinstance(obj, dict):
    _res = {}
    for k in obj.keys():
      try:
        _res[str(k)] = decode(obj[k], depth)
      except:
        _res[unicode(k)] = decode(obj[k])
    return _res
  elif isinstance(obj, list):
    _res = []
    for i in obj:
      _res.append(decode(i))
    return _res
  elif not obj:
    return None
  else:
    try: 
      return unicode(obj)
    except:
      return obj

def encoode(obj):
  if isinstance(obj, dict):
    _res = json.dumps(obj)
    for k in obj.keys():
      _res[str(k)] = decode(obj[k])
      return _res
  elif isinstance(obj, list):
    _res = json.dumps(obj)
    for i in obj:
      _res.append(decode(i))
    return _res
  elif not obj:
    return None
  else:
    return json.dumps(obj)

def decodes(obj):
  if isinstance(obj, dict):
    _res = {}
    for k in obj.keys():
      _res[str(k)] = decodes(obj[k])
