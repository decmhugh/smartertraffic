from django.conf.urls import patterns, include, url

from django.contrib import admin
import smartcity.web.settings as settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    (r'^api/hello_world/$', 'smartcity.web.controls.views.hello_world'),
    (r'^api/traffic/$', 'smartcity.web.controls.views.traffic'),
    (r'^api/analyse/$', 'smartcity.web.controls.views.analyse'),
    (r'^api/twitter/$', 'smartcity.web.controls.views.twitter'),
    (r'^api/twitterresult/$', 'smartcity.web.controls.views.twitterresult'),
    (r'^api/distribution/$', 'smartcity.web.controls.views.distribution'),
    (r'^api/dist_wd/$', 'smartcity.web.controls.views.distribution_weekday'),
    (r'^api/dist_we/$', 'smartcity.web.controls.views.distribution_weekend'),
    (r'^api/tweetcloud_aa/$', 'smartcity.web.controls.views.tweetcloud_aa'),
    (r'^api/weather/$', 'smartcity.web.controls.views.weather_corr'),
    (r'^api/trafficresult/$', 'smartcity.web.controls.views.trafficresult'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
