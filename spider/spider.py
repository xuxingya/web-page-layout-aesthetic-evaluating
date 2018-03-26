from pymongo import MongoClient
from utils import decode
from ghost import Ghost
from  models  import ProxyContent
from models import ProxyLinks
from models import DOMNode
from models import VisualBlock
from models import Feature
from urlparse import urljoin
import re
import json
import random
import time

DEPTH_PER_SITE = 5
DEPTH_PER_DOMIAN = 5

client = MongoClient()
db = client.design_mining
ghost = Ghost()


def create_tasks(urls):
  pass


def finish_task(url):
  pass


def startURL(url): 
  page, resources = ghost.open(url)
 
  print "now parsing " + url
  result, resources = ghost.evaluate(
    """
      as = document.querySelectorAll('a');
      
      var achor_list = [];

      for(i=0;i<as.length;i++){
        if(as[i] && as[i].attributes.href){
          achor_list.push(as[i].attributes.href.value);
        }
      }

      achor_list;
    """
  )
  time.sleep(2)
  print "geting doms: " + url

  time.sleep(random.randint(5, 15))

  clean_p = re.compile(r'#.*$|\?.*$')
  prefix_p = re.compile(r'^http://|https://')
  archor_list = decode(result)
  
  forword_urls = []

  print "anailsysing urls: " + url

  if not archor_list: archor_list = []

  for item in archor_list:
    if item and not item.startswith("javascript:"):
      item = clean_p.sub("", item)
      if not prefix_p.match(item):
        item = urljoin(url, item)

    forword_urls.append(item)
   
  print "finished and saving: " + url
  return forword_urls


def clean_url(url):
  if len(url.split('://'))==1:
    return ""
  main = url.split('://')[1]
  depth = main.split('/')[:2]
  if not depth[-1]:
    depth = depth[:-1]
  return str('/'.join(depth))

def save_to_db(url):
  VisualBlock.create() 

def control(starturl):
  urls = [starturl,]
  posed_urls = ["",]
  while urls:
    url = urls.pop(0)
    posed_urls.append(clean_url(url))
    time.sleep(1)
    if url:
      try:
        _us = startURL(url)
        for _u in _us:
          if (clean_url(_u) not in urls) and (clean_url(_u) not in posed_urls):
            urls.append(_u)
        if len(urls) > 1000:
          fo = open('urls.json', 'wb')
          fo.write(json.dumps(urls))
          fo.close()
          u = urls.pop(0)
          urls = [u, posed_urls, url.pop()]
          page = ProxyContent.create(
            url = url,
            content = _us,
            status = 0
            )
          ProxyLinks.create(
            page_id = page.id,
            resource_id = 0
            )

          
      except Exception , e:
        print e
      
  
if __name__ == '__main__':
  control("http://www.hao123.com")
