from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^login', views.login, name='login'),
    url(r'^logout$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^sakura$', views.sakura, name='sakura'),
    url(r'^add_picture$', views.add_picture, name='add_picture'),
    url(r'^delete_picture$', views.delete_picture, name='delete_picture'),
]
