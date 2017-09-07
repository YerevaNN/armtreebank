from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^process/$', views.TokenizationProcess.as_view(), name='process'),
  url(r'^process/result/$', views.process_result, name='process_result'),
  url(r'^bibliography/(?P<biblg_id>[0-9]+)/$', views.tokenize_bibliography, name='tokenize_bibliography'),
  url(r'^tag/bibliography/(?P<biblg_id>[0-9]+)/$', views.tag_bibliography, name='tag_bibliography'),
  url(r'^tokens/(?P<biblg_id>[0-9]+)/$', views.BiblgTokensView.as_view(), name='biblg_tokens'),
  url(r'^tokens/(?P<biblg_id>[0-9]+)/sentence/(?P<sentence_number>[0-9]+)/$', views.sentence_tokens, name='sentence_tokens'),
  url(r'^token/submit/$', views.token_submit, name='token_submit'),
  url(r'^token/submit/(?P<word_pos>[0-9]+)/$', views.token_submit_word, name='token_submit_word'),
  url(r'^word/new/$', views.new_word, name='new_word'),
  url(r'^word/overview/$', views.word_overview, name='word_overview'),
]
