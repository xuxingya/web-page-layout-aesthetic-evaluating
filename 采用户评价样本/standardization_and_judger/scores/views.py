# Create your views here.
from django.shortcuts import render_to_response

def score(request):
  return render_to_response('score.html', {})
