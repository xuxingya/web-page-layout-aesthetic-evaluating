# Create your views here.

from evaluation.models import (
  StyleComparison,
  UserInfo,
  StyleOrder,
  ComparisonWorker,
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
  print sc.subj.base_url, sc.obj.base_url, sc.order,
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
 
  cp = StyleComparison.objects.filter(user=user, status=0, type=0)
  if cp.count():
    fcp = cp[0]
    fcp.status = 1
    fcp.save() 
    return fcp.dump(True)
 
  cp = StyleComparison.objects.filter(user=user, status=1, type=0)
  if cp.count():
    return cp[0].dump(True)
 

  # generate orders
  orders = list(StyleOrder.objects.filter(user=user).all())
  untracked_screenshorts = WebScreenshort.objects.exclude(id__in=[o.web.id for o in orders])

  _current = len(orders)
  for us in untracked_screenshorts:
    _current += 1
    order = StyleOrder.objects.create(user=user, web=us, order=_current)
    orders.append(order)

  orders = sorted(orders, key=lambda x: x.order)
 
  worker_list = list(user.workers.all())
  if len(worker_list) == 0:
    worker_list.append(ComparisonWorker.objects.create(
      user=user, 
      left=0, 
      right=len(orders)-1,
      count=cnt(len(orders)))) 
  
  sorting_type = int(request.GET.get('type', '0'))

  while len(worker_list)>0:
    worker = worker_list.pop(0)
    i = worker.left
    j = worker.right
    print "[", i, ",", j, "] start,", len(worker_list), "workers remain"
    if j-i<=5:
      mid = orders[(i+j)/2]
    else:
      if worker.txt != None:
        _l = json.loads(worker.txt)
      else:
        _l = random.sample(range(i,j), 5)
        worker.txt = json.dumps(_l)
        worker.save()
      tasks = []
      for _i in _l:
        for _j in _l:
          if _i==_j:
            continue
          subj = orders[_i]
          obj = orders[_j]
          sc = StyleComparison.objects.filter(
            Q(subj=subj.web, obj=obj.web)\
            |Q(subj=obj.web, obj=subj.web), user=user)
          if sc.count() == 0:
            tasks.append(StyleComparison.objects.create(
              user=user,
              subj=subj.web,
              obj=obj.web,
              order=0,
              type=0,
              status=0))
            tasks.append(StyleComparison.objects.create(
              user=user,
              subj=subj.web,
              obj=obj.web,
              order=0,
              type=1,
              status=0))
          elif sc.filter(type=sorting_type).count()==0:
            tasks.append(StyleComparison.objects.create(
              user=user,
              subj=subj.web,
              obj=obj.web,
              type=sorting_type,
              status=0))
      if len(tasks)!=0:
        ft = tasks[0]
        ft.status=1
        ft.save()
        return ft.dump(True)

      for _i in range(4):
        for _j in range(_i+1,5):
          subj = orders[_l[_i]]
          obj = orders[_l[_j]]
          sc = StyleComparison.objects.filter(
            Q(subj=subj.web, obj=obj.web)\
            |Q(subj=obj.web, obj=subj.web), user=user)\
            .filter(type=sorting_type).all()[0]
          if cmp(sc, subj) == 0:
            _t = _l[_i]
            _l[_i] = _l[_j]
            _l[_j] = _t
      mid = orders[_l[2]] 
    
    tasks = []
    scs = []
    for order in orders:
      if order == mid:
        scs.append(None)
        continue
      sc = StyleComparison.objects.filter(Q(subj=mid.web, obj=order.web)|Q(subj=order.web, obj=mid.web), user=user)
      if sc.count()==0:
        tasks.append(StyleComparison.objects.create(
          user=user,
          subj=mid.web,
          obj=order.web,
          order=0,
          type=0,
          status=0))
        tasks.append(StyleComparison.objects.create(
          user=user,
          subj=mid.web,
          obj=order.web,
          order=0,
          type=1,
          status=0))
      elif sc.filter(type=sorting_type).count()==0:
        tasks.append(StyleComparison.objects.create(
          user=user,
          subj=mid.web,
          obj=order.web,
          type=sorting_type,
          status=0))
      else:
        scs.append(sc.filter(type=sorting_type).all()[0])
    if len(tasks):
      ft = tasks[0]
      ft.status=1
      ft.save()
      return ft.dump(True)

    changed = []

    while i<=j: 
      while cmp(scs[i], mid) == 2:
        i+= 1
      while cmp(scs[j], mid) == 0:
        j-= 1
      if i<=j:
        print i,j
        if i!=j:
          _tmp = scs[i]
          scs[i] = scs[j]
          scs[j] = _tmp
          _tmp = orders[i].order
          orders[i].order = orders[j].order
          orders[j].order = _tmp
          if orders[i] not in changed:
            changed.append(orders[i])
          if orders[j] not in changed:
            changed.append(orders[j])
          _tmp = orders[i]
          orders[i] = orders[j]
          orders[j] = _tmp

        i += 1
        j -= 1
    
    if worker.left<j:
      worker_list.append(
        ComparisonWorker.objects.create(
          left = worker.left,
          right = j,
          user=user,
          count=cnt(j-worker.left+1)
        ))
    if worker.right>i:
      worker_list.append(
        ComparisonWorker.objects.create(
          left = i,
          right = worker.right,
          user=user,
          count = cnt(worker.right-i+1)
        ))
    worker.delete()
    for c in changed:
      c.save()
    print "[", i, ",", j, "] ends"
  # finished the works 
  return [so.web.dump() for so in orders]


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
