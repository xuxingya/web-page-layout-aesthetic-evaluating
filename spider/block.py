from ghost import Ghost
from utils import decode
import os
import random
from pymongo import MongoClient
import Image
import traceback
import colorsys

client = MongoClient()
db = client.blocks
block_text = db["block_text"]

def render_notext(url):
  sitename = url.replace('.', '_').replace('/','+').strip()
  if os.path.isfile("texts/text/"+ sitename + '.png'):
    return

  block_text.remove({ 'sitename': sitename })

  ghost = Ghost(viewport_size=(1280, 700), wait_timeout=60)
  ghost.set_proxy('https', port=8118)
  ghost.open("http://"+url, headers={
    "Accept":"image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    })
 
  ghost.wait_for_page_loaded()
  #time.sleep(10)
  if not os.path.isfile("texts/text/"+ sitename + '.png'):
    ghost.capture_to("texts/text/"+ sitename +'.png',(0,0,1280,700))
  else:
    return


  ghost.evaluate("""
    var _stack = [document.getElementsByTagName("body")[0], ];
    _stack[0].depth = 0;
    var _max_dp = 0;
    var currentId = 0;

    function findPos(obj) {
        var curleft = curtop = 0;
        if (obj.offsetParent) {
          do {
            curleft += obj.offsetLeft;
            curtop += obj.offsetTop;
          }while (obj = obj.offsetParent);
        }
        return [curleft,curtop];
    }
  """)

  slen, _res = ghost.evaluate("_stack.length")
  nodes = []
  while slen > 0:
    ghost.evaluate(
      """
        var currentNode = _stack.pop();
        currentNode.relativeId = currentId;
        if(currentId==0){
          currentNode.parentId = false;
        }
        currentId ++;
        if(currentNode.depth > _max_dp){
          _max_dp = currentNode.depth;
        } 
        if(currentNode.style != undefined){
          currentNode.style.color = "rgba(0,0,0,0)";
          currentNode.style.color = "rgba(0,0,0,0) !important";
          currentNode.style["text-shadow"] = "none";
        }
        if(currentNode.attributes != undefined){
          currentNode.attributes.placeholder = "";
        }
        
        var innerTextLength = 0;
        for(i=0;i<currentNode.childNodes.length;i++){
          if (currentNode.childNodes[i].nodeType!=3 && currentNode.childNodes[i].nodeType!=8){
            currentNode.childNodes[i].depth = currentNode.depth + 1;
            currentNode.childNodes[i].parentId = currentNode.relativeId;
            _stack.push(currentNode.childNodes[i]);
          } 
          if(currentNode.childNodes[i].nodeType==3 && currentNode.childNodes[i].nodeValue && currentNode.childNodes[i].nodeValue.trim()){
            innerTextLength += 1;
          }
        }
        try{
          if (currentNode.tagName && currentNode.tagName.toLowerCase() =='iframe'){
            var idoc = currentNode.contentDocument.getElementsByTagName("body")[0];
            idoc.depth = currentNode.depth + 1;
            _stack.push(idoc);
          }
        }catch(e){
            currentNode.style.opacity = 0;
        }
    """)
    itl, _res = ghost.evaluate("innerTextLength")
    if itl>=0:
      style, resources = ghost.evaluate(
        'getComputedStyle(currentNode);'
      )
      text, resources = ghost.evaluate(
        'currentNode.innerText;'
      )
      nodeName, resources = ghost.evaluate(
        'currentNode.nodeName;'
      )
      parentId, resources = ghost.evaluate(
        'currentNode.parentId;'
      )
      currentId, resources = ghost.evaluate(
        'currentNode.relativeId;'
      )
      width, resources = ghost.evaluate(
        'currentNode.offsetWidth;'
      )
      height, resources = ghost.evaluate(
        'currentNode.offsetHeight;'
      )
      top, resources = ghost.evaluate(
      """
        var __tl = findPos(currentNode);
        __tl[1];
      """
      )
      left, resources = ghost.evaluate(
        '__tl[0];'
      )
      if top<700 and left<1280:
        pl, resources = ghost.evaluate(
          'getComputedStyle(currentNode).paddingLeft;'
        )
        pr, resources = ghost.evaluate(
          'getComputedStyle(currentNode).paddingRight;'
        )
        pt, resources = ghost.evaluate(
          'getComputedStyle(currentNode).paddingTop;'
        )
        pb, resources = ghost.evaluate(
          'getComputedStyle(currentNode).paddingBottom;'
        )
        d, resources = ghost.evaluate(
          'currentNode.depth;'
        )

        if width*height>0:
          nodes.append({
            'nodeStyle': decode(style),
            'nodeText': decode(text),
            'nodeName': decode(nodeName),
            'pos': map(int,(top, left, width, height)),
            'padding': map(lambda x: int(x.replace('px','')), (pl,pr,pt,pb)),
            'depth': d,
            'parentId': parentId,
            'currentId': currentId,
          })
          print "A node of", decode(nodeName), "effects"
    slen, _res = ghost.evaluate("_stack.length")
      

  ghost.capture_to("texts/notext/"+ sitename +'.png', (0,0,1280,700))
  max_d, resources = ghost.evaluate('_max_dp;')
  im = Image.open('texts/notext/'+ sitename + '.png')
  pxs = im.load()
  idMaps = {}
  for node in nodes:
    l = block_text.count() + 1
    idMaps[node['currentId']] = l
    region = (node["pos"][0]+node["padding"][2], #top
              node["pos"][1]+node["padding"][0], #left
              node["pos"][2]-node["padding"][0]-node["padding"][1], #width
              node["pos"][3]-node["padding"][2]-node["padding"][3]) #height
    node.update({
      'textRegion': region,
      'sitename': sitename,
      'id': l,
      'parent': idMaps.get(node['parentId'], None) if node['parentId'] else None,
    })
    for i in xrange(region[0], region[0]+region[3]):
      if i < 0:
        continue
      if i >= 700:
        break
      for j in xrange(region[1], region[1]+region[2]):
        if j< 0:
          continue
        if j>=1280:
          break
        try:
          _c = node["depth"]*1.0/max_d
          r,g,b = map(lambda x: int(x*255), colorsys.hsv_to_rgb(_c, 1, 1))
          pxs[j,i] = (r,g,b)
        except:
          print im.size
          print i,j
          print (int(i/700.0*255),int(j/1280.0*255), int(node["depth"]))
          raise
    im.save('texts/notext/'+ sitename + '.png')    
    block_text.insert(node)

  
  ghost.evaluate(
    """
    var _stack = [document.getElementsByTagName("body")[0], ];
    while(_stack.length>0){
      var currentNode = _stack.pop();
      if(currentNode.style != undefined){
          currentNode.style["background-image"] = "none";
      }

      for(i=0;i<currentNode.childNodes.length;i++){
        _stack.push(currentNode.childNodes[i]);
      }
      try{
        if (currentNode.tagName && currentNode.tagName.toLowerCase() =='iframe'){
          _stack.push(currentNode.contentDocument.getElementsByTagName("body")[0]);
        }
      }catch(e){
        currentNode.style.opacity = 0;
      }
    }

    var imgs = document.getElementsByTagName('img');
    for(i=0;i<imgs.length;i++){
      imgs[i].style.opacity = 0;
    }
    """)

  if not os.path.isfile('texts/nopic/'+sitename+'.png'):
    ghost.capture_to("texts/nopic/"+sitename+'.png',(0,0,1280,700))

  ghost.evaluate(
    """
    var _stack = [document.getElementsByTagName("body")[0], ];
    while(_stack.length>0){
      var currentNode = _stack.pop();
      if( getComputedStyle(currentNode) && getComputedStyle(currentNode).cssText && getComputedStyle(currentNode).cssText.indexOf('gradient')>-1 ){
            currentNode.style.background="#fa37d3";
        }
      for(i=0;i<currentNode.childNodes.length;i++){
        _stack.push(currentNode.childNodes[i]);
      }
      try{
        if (currentNode.tagName && currentNode.tagName.toLowerCase() =='iframe'){
          _stack.push(currentNode.contentDocument.getElementsByTagName("body")[0]);
        }
      }catch(e){
        currentNode.style.opacity = 0;
      }
    }
    """)

  if not os.path.isfile('texts/nogradient/'+sitename+'.png'):
    ghost.capture_to('texts/nogradient/' + sitename +'.png',(0,0,1280,700))


class PixelCounter(object):
  ''' loop through each pixel and average rgb '''
  def __init__(self, imageName):
      self.pic = Image.open(imageName)
      # load image data
      self.imgData = self.pic.load()
  def averagePixels(self, t,l,w,h):
      r, g, b = 0, 0, 0
      count = 0
      for x in xrange(l,l+w):
          for y in xrange(t, t+h):
              tempr,tempg,tempb = self.imgData[x,y][:3]
              r += tempr
              g += tempg
              b += tempb
              count += 1
      # calculate averages
      return (r/count), (g/count), (b/count), count


if __name__ == '__main__':
  #top = open('todo_site.txt', 'rb').read().split('\n')
  random.seed()
  #top = ["http://wordreference.com"]
  top = os.listdir('/home/gsj987/experiment/webscorer.new/media/')
  top = map(lambda x: x.replace('_g.png', '').replace('_', '.'), filter(lambda y: y.endswith('.png'), top)) 
  random.shuffle(top)

  for t in top:
    print t
    t = t.replace("http://", "").replace("https://", "").strip()
    try:
      render_notext(t)
    except Exception,e :
      sitename = t.replace('.', '_').replace('/','+')+'.png'
      print sitename, e
      if(os.path.isfile("texts/text/"+sitename)):
       os.unlink("texts/text/"+sitename)
      if(os.path.isfile("texts/notext/"+sitename)):
        os.unlink("texts/notext/"+sitename)
      if(os.path.isfile("texts/nopic/"+sitename)):
        os.unlink("texts/nopic/"+sitename)
      if(os.path.isfile("texts/nogradient/"+sitename)):
        os.unlink("texts/nogradient/"+sitename)
      
      traceback.print_exc()
