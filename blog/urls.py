from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^sakura$', views.sakura, name='sakura'),
    url(r'^add_picture$', views.add_picture, name='add_picture'),
    url(r'^delete_picture$', views.delete_picture, name='delete_picture'),
    url(r'^new_novels', views.new_novels, name='new_novels'),
]
