from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles import views as static_views

from core import views as core_views

urlpatterns = [
  url(r'static/(?P<path>.*)$', static_views.serve),
  url(r'^admin/', admin.site.urls),
  url(r'^$', core_views.HomePageView.as_view() , name='home'),
  url(r'^about/$', core_views.AboutPageView.as_view() , name='about'),
  url(r'^morph/$', core_views.MorphPageView.as_view() , name='morph'),
  url(r'^user/', include('user.urls')),
  url(r'^bibliography/', include('bibliography.urls')),
  url(r'^tokenization/', include('tokenization.urls')),
]

