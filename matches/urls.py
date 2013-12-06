from django.conf.urls import patterns, url

from matches import views

urlpatterns = patterns('',
					   url(r'^$', views.index, name = "index"),
					   url(r'^register', views.register, name = "register"),
					   url(r'^player/(?P<player_id>\d+)/$', views.player, name = "player"),
					   url(r'^match/(?P<match_id>\d+)/$', views.match, name = "match"),
					   );