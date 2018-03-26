from classify.models import Classify
from django.core.urlresolvers import reverse
from evaluation.models import (
  UserInfo, 
  WebScreenshort,
  )
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import (
  render_to_response,
  get_object_or_404,
  redirect,
  )
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import time
import hashlib



def classify_page(request):
  if request.method == 'POST':
    d = request.POST
    un = d.get('username')
    age = d.get('age', None)
    gender = d.get('gender', None)
    
    if not un:
      return HttpResponseBadRequest(repr(request.POST))

    try:
      user = UserInfo.objects.get(username=un)
    except UserInfo.DoesNotExist:
      if age is None or gender is None:
        return HttpResponseBadRequest()
      user = UserInfo.objects.create(
          username=un,
          age=int(age),
          gender=int(gender)
      )
    return redirect(reverse('classify.views.set_web')+'?uid='+user.username)


  return render_to_response(
    "cindex.html", {}, context_instance=RequestContext(request))

def set_web(request):
  uid = request.GET.get("uid")
  user = get_object_or_404(UserInfo, username=uid) 
  
  cid = request.GET.get("cid")
  if cid:
    c = get_object_or_404(Classify, id=int(cid))

    type = request.GET.get("type")
    if type:
      c.type = int(type)
      c.status = 1
      c.save()

  ws = WebScreenshort.objects.exclude(classifies__in=user.classifies.filter(status=1).all())
  if ws.count()==0:
    return render_to_response(
      "cdone.html", {})
  cs = Classify.objects.filter(status=0)
  if cs.count():
    c = cs[0]
  else:
    c = Classify.objects.create(
      web=ws[0],
      user=user)
  return render_to_response(
    "cset_web.html", {'c': c, 'uid': uid})