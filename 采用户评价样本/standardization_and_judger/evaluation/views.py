# Create your views here.

from evaluation.models import (
  StyleComparison,
  UserInfo,
  StyleOrder,
  UpDownWorker,
  WebScreenshort,
)
from django.db.models import Q, F
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
import json
import math
import random
random.seed()

def json_dump(func):
  def wrapper(request, *args, **kwargs):
    response = func(request, *args, **kwargs)
    if isinstance(response, HttpResponse):
      return response
    return HttpResponse(json.dumps(response), mimetype="application/json")

  return wrapper

def cnt(num):
  if num<=0:
    return 0
  else:
    return int(num*math.log(num,2))

def cmp(sc, mid):
  if sc==None:
    return 1
  if sc.subj == mid.web:
    return sc.order
  else:
    return 2-sc.order

@json_dump
def sort_worker(request):
  uid = request.GET.get('uid')
  if not uid:
    return  HttpResponseBadRequest()

  user = UserInfo.objects.get(pk=uid) 
  sorting_type = int(request.GET.get('type', '0'))

  cp = StyleComparison.objects.filter(user=user, status=0, type=sorting_type)
  if cp.count():
    fcp = cp[0]
    fcp.status = 1
    fcp.save() 
    return fcp.dump(True)
 
  cp = StyleComparison.objects.filter(user=user, status=1, type=sorting_type)
  if cp.count():
    return cp[0].dump(True)
 

  # generate orders
  orders = list(StyleOrder.objects.filter(user=user).all())
  untracked_screenshorts = list(WebScreenshort.objects.exclude(id__in=[o.web.id for o in orders]))

  if not len(orders):
    _web_id = int(random.random() * len(untracked_screenshorts))
    _web = untracked_screenshorts.pop(_web_id)
    orders.append(StyleOrder.objects.create(
      web=_web,
      user=user,
      order=0))

  orders = sorted(orders, key=lambda x: x.order)
 
  worker_list = list(user.workers.all())

  if len(worker_list) == 0:
    if not len(untracked_screenshorts):
      return [sd.web.dump() for sd in orders]
    _web = untracked_screenshorts.pop(int(random.random() * len(untracked_screenshorts)))
    worker_list.append(UpDownWorker.objects.create(
      user=user,
      left=0,
      right=len(orders)-1,
      web=_web
      ))
      
      
  while len(worker_list)>0:
    worker = worker_list.pop(0)
    l = worker.left
    r = worker.right

    mid = (l+r)/2
    
    subj = worker
    obj = orders[mid]

    tasks = []
    scs = None
    sc = StyleComparison.objects.filter(
      Q(subj=subj.web, obj=obj.web)\
      |Q(subj=obj.web, obj=subj.web), user=user).filter(type=sorting_type)
    if sc.count()==0:
      tasks.append(StyleComparison.objects.create(
        user=user,
        subj=subj.web,
        obj=obj.web,
        type=sorting_type,
        status=0))
    else:
      scs = sc[0]
    if len(tasks)!=0:
      ft = tasks[0]
      ft.status=1
      ft.save()
      return ft.dump(True)
 
    if cmp(scs, subj)==2:
      new_l = l
      new_r = int((l+r)*0.6)
      if new_r >= r: new_r = r-1
    else:
      new_l = int((l+r)*0.4)
      if new_l <= l: new_l = l+1
      new_r = r

    if new_r-new_l<0:
      new_o = new_l
      if new_o<0: new_o=0
      if new_o>len(orders): new_o = len(orders)
      StyleOrder.objects.filter(user=user, order__gte=new_o).update(order=F('order')+1)
      StyleOrder.objects.create(user=user, web=subj.web, order=new_o)

      worker.delete()
      
      return sort_worker(request)
    else:
      worker.left = new_l
      worker.right = new_r

      worker.save()
      worker_list.append(worker)

  return sort_worker(request)


def set_order(request):
  uid = request.GET.get('uid') 
  sid = request.GET.get('sid')
  order = request.GET.get('order')
  if not (uid and sid and order):
    return HttpResponseBadRequest()
  user = get_object_or_404(UserInfo, username=uid)
  sc = get_object_or_404(StyleComparison, id=int(sid), user=user)
  
  sc.order = order
  sc.status = 2
  sc.save()
  
  return sort_worker(request)


@json_dump
def start(request):
  username = request.GET.get('un')
  age = request.GET.get('age', None)
  gender = request.GET.get('gender', None)

  if not username:
    return HttpResponseBadRequest()

  try:
    user = UserInfo.objects.get(username=username)
  except UserInfo.DoesNotExist:
    if age is None or gender is None:
      return HttpResponseBadRequest()
    user = UserInfo.objects.create(
      username=username,
      age=int(age),
      gender=int(gender)
      )
  
  return {
    'uid': user.pk
  }


def home_page(request):
  return render_to_response(
    'index.html', {})

def show_results(request):
  users = StyleOrder.objects.values('user').distinct()
  return render_to_response(
    'results.html', {
      'users': users, 
      })
