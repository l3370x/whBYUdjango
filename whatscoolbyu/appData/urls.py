from django.conf.urls import *


urlpatterns = patterns('appData.views',
			url(r'^home/$', 'Home'),
			url(r'^$', 'Home'),
			)
