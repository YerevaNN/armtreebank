from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^process/$', views.TokenizationProcess.as_view(), name='process'),
  url(r'^process/result/$', views.process_result, name='process_result'),
]
