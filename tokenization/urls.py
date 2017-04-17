from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^process/$', views.TokenizationProcess.as_view(), name='process'),
  url(r'^process/result/$', views.process_result, name='process_result'),
  url(r'^bibliography/(?P<biblg_id>[0-9]+)/$', views.tokenize_bibliography, name='tokenize_bibliography'),
  url(r'^tokens/(?P<biblg_id>[0-9]+)/$', views.BiblgTokensView.as_view(), name='biblg_tokens'),
]
