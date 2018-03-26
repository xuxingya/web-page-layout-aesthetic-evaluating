from django.contrib import admin
from evaluation.models import WebScreenshort


class WebScreenshortAdmin(admin.ModelAdmin):
  list_display = ('base_url', 'is_active')


admin.site.register(WebScreenshort, WebScreenshortAdmin)
