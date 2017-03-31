from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.forms import Form
from django.template import Template, Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Text, Author, Bibliography, Textbook, Fiction, Press 
from core.functions import base_context
from user.models import UserProfile
import bibliography.forms as BiblForms

class BibliographyListView(View):
  
  def get(self, request, page = 1):
    biblg_list = Bibliography.objects.all()
    paginator = Paginator(biblg_list, 10)
    
    try:
      biblgs = paginator.page(page)
    except PageNotAnInteger:
      biblgs = paginator.page(1)
    except EmptyPage:
      biblgs = paginator.page(paginator.num_pages)
    
    context = base_context(request)
    context['biblg_list'] = biblgs
    
    return render(request, 'bibliography_list.html', context)

class BibliographyCreate(View):
  def get(self, request):
    context = base_context(request)
    context['text_form'] = BiblForms.TextForm
    context['textbook_form'] = BiblForms.TextbookForm
    context['fiction_form'] = BiblForms.FictionForm
    context['press_form'] = BiblForms.PressForm
    return render(request, 'bibliography_form.html', context)

def bibliography_save(request):
  response = {
    'type': 'error',
    'response': 'Սխալմունք'
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  form = request.POST
  type = form.get('type')
  
  if type == 'textbook':
    
    if int(form.get('texts_count')) == 0:
      response['response'] = 'Ավելացրեք տեքստ'
      return JsonResponse(response)
    
    text = Text.save_text(form, True, count=int(form.get('texts_count')))
    if text['type'] == 'error':
      return JsonResponse(text)
    
    text = text['text']
    if isinstance(text, list) == False:
      text = [text]
    
    textbook = Textbook()
    textbook.profile = UserProfile.objects.get(user=request.user)
    textbook.name = form.get('name')
    textbook.tokens_count = form.get('tokens_count')
    textbook.text_creation_date = textbook.valid_date(form.get('text_creation_date'))
    textbook.text_publication_date = textbook.valid_date(form.get('text_publication_date'))
    textbook.sphere = form.get('sphere')
    textbook.license = form.get('license')
    
    try:
      textbook.clean_fields()
      textbook.save()
      
      for t in text:
        textbook.texts.add(t)
      
      if len(form.getlist('author[]')) == 0:
        raise Exception('Նշեք հեղինակին')
      
      for a in form.getlist('author[]'):
        if a:
          textbook.author.add(a)
      
      textbook.clean_fields()
      textbook.save()
      
      response = {
        'type': 'ok',
        'response': 'Դասգիրքը ստեղծված է'
      }
    except Exception as E:
      for t in text:
        t.delete()
      response['response'] = 'Սխալմունք: {e}'.format(e=E)
      return JsonResponse(response)
    
  elif type == 'fiction':
  
    text = Text.save_text(form, True)
    if text['type'] == 'error':
      return JsonResponse(text)
    
    text = text['text']
    
    fiction = Fiction()
    fiction.profile = UserProfile.objects.get(user=request.user)
    fiction.text = text
    fiction.name = form.get('name')
    fiction.tokens_count = form.get('tokens_count')
    fiction.genre = form.get('genre')
    fiction.text_creation_date = fiction.valid_date(form.get('text_creation_date'))
    fiction.text_publication_date = fiction.valid_date(form.get('text_publication_date'))
    fiction.mediation = form.get('mediation')
    fiction.translation_original = form.get('translation_original')
    fiction.translation_mediator = form.get('translation_mediator')
    fiction.license = form.get('license')
    
    try:
      fiction.clean_fields()
      fiction.save()
      
      for t in form.getlist('translation[]'):
        if t:
          fiction.translation.add(t)
      
      fiction.save()
      response = {
        'type': 'ok',
        'response': 'Գեղ. գիրքը ստեղծված է'
      }
    except Exception as E:
      text.delete()
      response['response'] = 'Սխալմունք: {e}'.format(e=E)
      return JsonResponse(response)
      
  elif type == 'press':
    
    text = Text.save_text(form, False)
    if text['type'] == 'error':
      return JsonResponse(text)
    
    text = text['text']
    
    press = Press()
    press.profile = UserProfile.objects.get(user=request.user)
    press.text = text
    press.name = form.get('name')
    press.tokens_count = form.get('tokens_count')
    press.text_publication_date = press.valid_date(form.get('text_publication_date'))
    press.number = form.get('number')
    press.sphere = form.get('sphere')
    press.type = form.get('press_type')
    press.link = form.get('link')
    press.license = form.get('license')
    
    try:
      press.clean_fields()
      press.save()
      response = {
        'type': 'ok',
        'response': 'Մամուլը ստեղծված է'
      }
    except Exception as E:
      text.delete()
      response['response'] = 'Սխալմունք: {e}'.format(e=E)
      return JsonResponse(response)
      
  else:
    response['response'] = 'Նշեք մատենագրության տիպը'
    return JsonResponse(response)
    
  return JsonResponse(response)

def author_save(request):
  response = {
    'type': 'error',
    'response': 'Սխալմունք'
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
    
  form = request.POST
  author_form = {
    'author_name': form.get('author_name'),
    'author_patronymic': form.get('author_patronymic'),
    'author_pseudonym': form.get('author_pseudonym'),
    'author_birth_date': form.get('author_birth_date'),
    'author_death_date': form.get('author_death_date'),
  }
  
  response = Author.create_author(request, form = author_form)
  
  return JsonResponse({
    'type': response['type'],
    'response': response['response'],
    'authors': Template('{{form.author}}').render(Context({'form': BiblForms.TextForm()})),
  })