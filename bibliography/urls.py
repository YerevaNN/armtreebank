from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.BibliographyView.as_view(), name='bibliography'),
  url(r'^(?P<type>[A-z]+)/(?P<page>[0-9]+)/$', views.BibliographyListView.as_view(), name='list_view_bibliography'),
  url(r'^create/$', views.BibliographyCreate.as_view(), name='create_bibliography'),
  url(r'^create/done/$', views.bibliography_save, name='create_done_bibliography'),
  url(r'^author/create/$', views.author_save, name='create_author'),
]
