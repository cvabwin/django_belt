from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wish_list$', views.wish_list),
    url(r'^new$', views.new),
    url(r'^create_wish$', views.create_wish), 
    url(r'^add_wish/(?P<id>\d+)$', views.add_wish),
    url(r'^remove_wish/(?P<id>\d+)$', views.remove_wish),
    url(r'^delete_wish/(?P<id>\d+)$', views.delete_wish),
    url(r'^display_item/(?P<id>\d+)$', views.display_item),
]
