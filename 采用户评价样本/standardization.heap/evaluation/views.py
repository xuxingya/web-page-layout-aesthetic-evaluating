# Create your views here.

from evaluation.models import (
  StyleComparison,
  UserInfo,
  StyleOrder,
  UpDownWorker,
  WebScreenshort,
)
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
import json
import math
import random
import json
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
  untracked_screenshorts = WebScreenshort.objects.exclude(id__in=[o.web.id for o in orders])

  _current = len(orders)
  for us in untracked_screenshorts:
    order = StyleOrder.objects.create(user=user, web=us, order=_current)
    _current += 1
    orders.append(order)

  orders = sorted(orders, key=lambda x: x.order)
  print user.status, user.cursor, user.sorted, [o.web.base_url for o in orders]
 
  worker_list = list(user.workers.all())
  bottom = len(orders)-user.sorted-1

  if len(worker_list) == 0:
    if user.status==1 and (user.sorted==len(orders) or bottom==0):
      # has finished
      return [so.web.dump() for so in orders]

    if user.status==1:
      # can select the top
      orders[0].order = bottom
      orders[0].save()
      orders[bottom].order = 0
      orders[bottom].save()
      user.sorted += 1
      user.cursor = 0
      user.save()
      bottom -= 1
      if bottom == 0:
        # finished again
        return [so.web.dump() for so in  sorted(orders, key=lambda x: x.order)]
      else:
        # new up-down work
        worker_list.append(UpDownWorker.objects.create(user=user, top=0))

    elif user.status==0:
      if user.cursor == 0:
        user.status = 1
        user.save()
        return sort_worker(request)
      if user.cursor == -1:
        user.cursor = bottom
        user.save()
      else:
        user.cursor -= 1
        user.save()
      worker_list.append(UpDownWorker.objects.create(user=user,top=user.cursor))
 
  while len(worker_list)>0:
    worker = worker_list.pop(0)
    top = worker.top

    tasks = []
    scs = []
    ranges = [top]
    if(top*2+1<=bottom):
      ranges.append(top*2+1)
    if(top*2+2<=bottom):
      ranges.append(top*2+2) 
    
    for i in range(len(ranges)):
      for j in range(i+1,len(ranges)):
        subj = orders[ranges[i]]
        obj = orders[ranges[j]]
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
          scs.append(sc[0])
    if len(tasks)!=0:
      ft = tasks[0]
      ft.status=1
      ft.save()
      return ft.dump(True)
 
    changed = top
    si = 0
    for i in ranges[1:]:
      if cmp(scs[si], orders[changed])==2:
        changed = i
        si = 2
      else:
        si = 1
    
    if changed!=top:
      orders[top].order=changed
      orders[top].save()
      orders[changed].order=top
      orders[changed].save()

      t = orders[top]
      orders[top]=orders[changed]
      orders[changed]=t
      print user.status, user.cursor, user.sorted, [o.web.base_url for o in orders]

      worker_list.append(UpDownWorker.objects.create(
        user=user,
        top=changed))

    worker.delete()
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
