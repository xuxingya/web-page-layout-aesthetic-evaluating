from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'evaluation.views.home_page', name='home'),
    url(r'^results$', 'evaluation.views.show_results', name='results'),
    url(r'^start$', 'evaluation.views.start', name='start'),
    url(r'^set$', 'evaluation.views.set_order', name='set'),
    url(r'^work$', 'evaluation.views.sort_worker', name='work'),
    url(r'^score$', 'scores.views.score'),

    url(r'^class/$', 'classify.views.classify_page'),
    url(r'^class/set$', 'classify.views.set_web'),


    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
