#_*_ coding: utf-8 _*_
from django.db import models
import os.path
from PIL import Image
from django.conf import settings
from django.db.models import Sum
# Create your models here.

class WebScreenshort(models.Model):
  base_url = models.CharField(max_length=150)
  is_active = models.BooleanField(default=True)
  screenshort = models.CharField(max_length=255)

  @property
  def grey_pic(self):
    img_path = self.screenshort.rsplit('.',1)[0] + '_g.' + self.screenshort.rsplit('.', 1)[1]
    full_path = os.path.join(settings.GIMG_PATH, img_path)
    if not os.path.isfile(full_path):
      org_file = os.path.join(settings.IMG_PATH, self.screenshort)
      _img = Image.open(org_file).convert('LA')
      _img.save(full_path)

    return img_path

  def dump(self):
    return {
      'name': self.base_url,
      'path': '/media/'+self.grey_pic,
      'id': self.id,
    }


class UserInfo(models.Model):
  age = models.SmallIntegerField(choices=((0, u"18-22"), (1, u"23-29"), (2, u"30-39"), (3, u"40以上")))
  gender = models.SmallIntegerField(choices=((0, u"男"), (1, u"女")))
  username = models.CharField(unique=True, primary_key=True, max_length=150)


class StyleComparison(models.Model):
  user = models.ForeignKey(UserInfo, related_name="cmps")
  subj = models.ForeignKey(WebScreenshort, related_name="comparion_subjects")
  obj = models.ForeignKey(WebScreenshort, related_name="comparion_objects")

  order = models.SmallIntegerField(choices=((0, "<"), (1, "=="), (2, ">")))
  type = models.SmallIntegerField(choices=((0, u"美感"), (1, u"复杂度")))
  status = models.SmallIntegerField(choices=((0, u"带评分"), (1, u"已分发"), (2, u"已完成")))

  def dump(self, need_count=False):
    _d = {
        'cid': self.id,
        'subj': self.subj.dump(),
        'obj': self.obj.dump(),
        'type': self.type
      }
    if need_count:
      _d.update({
        'workers' : ComparisonWorker.objects.filter(user=self.user).aggregate(Sum('count'))
      })
    return _d


class ComparisonWorker(models.Model):
  left = models.PositiveIntegerField()
  right = models.PositiveIntegerField()

  count = models.PositiveIntegerField()

  user = models.ForeignKey(UserInfo, related_name="workers")
  txt = models.TextField(blank=True, null=True)

class StyleOrder(models.Model):
  user = models.ForeignKey(UserInfo, related_name="orders")
  web = models.ForeignKey(WebScreenshort, related_name="orders")

  order = models.PositiveIntegerField()
