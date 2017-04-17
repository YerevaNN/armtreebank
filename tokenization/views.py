from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

from bibliography.models import Bibliography
from core.functions import base_context
from .models import Sentence, Token
from . import tokenizer

class TokenizationProcess(View):
  def get(self, request):
    context = base_context(request)
    return render(request, 'tokenization_process.html', context)
    
class BiblgTokensView(View):
  def get(self, request, biblg_id):
    context = base_context(request)
    biblg = get_object_or_404(Bibliography, id=biblg_id)
    context['biblg'] = biblg
    
    if hasattr(biblg, 'textbook'):
      texts = biblg.textbook.texts.all()
    elif hasattr(biblg, 'press'):
      texts = [biblg.press.text]
    elif hasattr(biblg, 'fiction'):
      texts = [biblg.fiction.text]
    
    context['texts'] = texts
    
    segments = []
    for text in texts:
      s_set = Sentence.objects.filter(text=text)
      for s in range(len(s_set)):
        t_set = [(t.position, t.token) for t in Token.objects.filter(sentence=s_set[s]).order_by('id')]
        segment = {
          'id': s+1,
          'segment': s_set[s].sentence,
          'tokens': t_set,
        }
        segments.append(segment)
    
    context['tokens'] = get_template('tokenization_output.html').render(Context({'segments': segments, 'color': 'blue'}))
    return render(request, 'tokenization_tokens_view.html', context)
    
def process_result(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
    'result': '',
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  text = request.POST.get('text')
  if not text:
    response['response'] = 'Ներմուծեք ինչ-որ տեքստ'
    return JsonResponse(response)
  
  try:
    T = tokenizer.Tokenizer(text)
    T.segmentation().tokenization()
    result = get_template('tokenization_output.html').render(Context({'segments': T.output(), 'color': 'teal'}))
  except Exception as E:
    response['response'] = 'Սխալմունք: {error}'.format(error=E)
    return JsonResponse(response)
  
  response = {
    'type': 'ok',
    'response': 'Մշակված է',
    'result': result,
  }
  return JsonResponse(response)
  
@csrf_exempt
def tokenize_bibliography(request, biblg_id):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
    
  try:
    biblg = Bibliography.objects.get(id=biblg_id)
  except Exception:
    response['response'] = 'Մատենագրությունը գտնված չէ'
    return JsonResponse(response)
  
  if biblg.tokenized != 'no':
    response['response'] = 'Մատենագրությունը արդեն թոքենիզացված է'
    return JsonResponse(response)
    
  if hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
    
  for text in texts:
    t = text.text
    try:
      T = tokenizer.Tokenizer(t)
      T.segmentation().tokenization()
      process = T.output()
    except Exception:
      pass
    
    i_s = 1
    for s in process:
      new_sentence = Sentence()
      new_sentence.text = text
      new_sentence.sentence = s['segment']
      new_sentence.position = i_s
      i_s += 1
      
      try:
        new_sentence.clean_fields()
        new_sentence.save()
      except Exception:
        pass
        
      for token in s['tokens']:
        new_token = Token()
        new_token.sentence = new_sentence
        new_token.token = token[1]
        new_token.position = token[0]
        
        try:
          new_token.clean_fields()
          new_token.save()
        except Exception:
          pass
          
  biblg.tokenized = 'yes'
  biblg.save()
  
  response = {
    'type': 'ok',
    'response': 'Թոքենիզացված է',
    'id': biblg_id,
  }
  return JsonResponse(response)