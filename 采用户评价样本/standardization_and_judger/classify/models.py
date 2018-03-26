#_*_ coding: utf-8 _*_
from django.db import models
from evaluation.models import (
  WebScreenshort,
  UserInfo,
  )


class Classify(models.Model):
  user = models.ForeignKey(UserInfo, related_name="classifies")
  web = models.ForeignKey(WebScreenshort, related_name="classifies")
  type = models.SmallIntegerField(choices=((0, u"好"),(1, u"差")), default=0)
  status = models.SmallIntegerField(choices=((0, u"ready"),(1, u"finished")), default=0)
