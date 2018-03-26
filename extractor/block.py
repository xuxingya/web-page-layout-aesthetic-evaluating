from ghost import Ghost
from utils import decode
import os
from pymongo import MongoClient
import traceback
import time

path = os.path.join(os.path.dirname(__file__), 'screenshot')
client = MongoClient()
db = client.blocks
block_text = db["block_evaluator"]

def get_sitename(url):
  url = url.replace("http://", "").replace("https://", "").strip()
  return url.replace('.', '_').replace('/', '+').strip() 

def render_notext(url):
  sitename = get_sitename(url)
  block_text.remove({ 'sitename': sitename })

  ghost = Ghost(viewport_size=(1280, 700), wait_timeout=60)
  ghost.set_proxy('https', port=8118)
  ghost.open(url, headers={
    "Accept":"image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    })
 
  ghost.wait_for_page_loaded()
  #time.sleep(10)
  ghost.capture_to(os.path.join(path,sitename +'.png'),(0,0,1280,700))

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
     
  block_text.remove({'sitename': sitename})

  idMaps = {}
  for node in nodes:
    l = str(int(time.time()*10000))
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
    block_text.insert(node)  
  return sitename

if __name__ == '__main__':
  t = "http://192.168.1.107:8887/4shared.com2.html"
  try:
    render_notext(t)
  except Exception,e :
    sitename = get_sitename(t) + '.png'
    print e
    if(os.path.isfile(os.path.join(path, sitename))):
     os.unlink(os.path.join(path, sitename))
    
    traceback.print_exc()
