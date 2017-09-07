from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

from .parser_noun import NounParserFactory
from .parser_verb import VerbParser
from tokenization.utils import st_count_all, st_count_biblg
from bibliography.models import Bibliography
from core.functions import base_context
from .models import Sentence, Token, Word, Noun, Verb
from . import tokenizer
from . import tagger

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
    
    context['st'] = st_count_biblg(biblg)
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
  
def tokenize_bibliography(request, biblg_id):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
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

def tag_bibliography(request, biblg_id):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  try:
    biblg = Bibliography.objects.get(id=biblg_id)
  except Exception:
    response['response'] = 'Մատենագրությունը գտնված չէ'
    return JsonResponse(response)
  
  if biblg.tokenized == 'no':
    response['response'] = 'Մատենագրությունը դեռ թոքենիզացված չէ'
    return JsonResponse(response)
    
  if biblg.tagged != 'no':
    response['response'] = 'Մատենագրությունը արդեն թագավորված է'
    return JsonResponse(response)
    
  if hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
    
  for text in texts:
    sentences = Sentence.objects.filter(text=text).order_by('position')
    for s in sentences:
      words = Token.objects.filter(sentence=s).order_by('id')
      for w in words:
        tgr = tagger.Tagger(w.token)
        tags = tgr.tag()
        if tags:
          for tag in tags:
            w.tag.add(tag)
          w.save()
          
  biblg.tagged = 'yes'
  biblg.save()
  
  response = {
    'type': 'ok',
    'response': 'Թագավորված է',
    'id': biblg_id,
  }
  return JsonResponse(response)

def sentence_tokens(request, biblg_id , sentence_number):  
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  try:
    biblg = Bibliography.objects.get(pk=biblg_id)
  except: 
    response['response'] = 'Biblg is not found.'
    return JsonResponse(response)
  
  if hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
  
  i = 0
  segment = {}
  
  sentence_number = int(sentence_number)
  if sentence_number < 1:
    sentence_number = 1

  for text in texts:
    sent = Sentence.objects.filter(text=text).filter(position=sentence_number)
    if len(sent):
      sent = sent[0]
      t_set = []
      for t in Token.objects.filter(sentence=sent).order_by('id'):
        if t.checked == False:
          t.tag.clear()
          tgr = tagger.Tagger(t.token)
          tags = tgr.tag()
          if tags:
            for tag in tags:
              t.tag.add(tag)
            t.save()
        daughters = []
        if t.tag:
          for tag in t.tag.all():
            if tag.pos == 'noun':
              daughters.append(('noun', Noun.objects.get(parent=tag),))
            elif tag.pos == 'verb':
              daughters.append(('verb', Verb.objects.get(parent=tag),))
              
        t_set.append((t.position, t.token, t, daughters))
      
      segment = {
        'position': sent.position,
        'segment': sent.sentence,
        'st': st_count_biblg(biblg)['sentence'][sent.position],
        'tokens': t_set,
      }
  
  response = {
    'type': 'ok',
    'response': 'Success.',
    'res': get_template('tokenization_biblg_output.html').render(Context({'biblg': biblg, 'segment': segment, 'auth': request.user.is_authenticated}))
  }
  return JsonResponse(response)
  
def token_submit(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  if not request.POST.get('biblg') or not request.POST.get('sentence') or not request.POST.get('token'):
    return JsonResponse(response)
  
  try:
    biblg = Bibliography.objects.get(id=request.POST.get('biblg'))
  except Exception:
    return JsonResponse(response)

    
  if hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
  
  s = 0
  for text in texts:
    sentences = Sentence.objects.filter(text=text).order_by('position')
    for s in sentences:
      s += 1
      if s == request.POST.get('sentence'):
        token = Token.objects.filter(sentence=s).filter(position=request.POST.get('token'))
        if token: 
          token = token[0]
          if len(token.tag.all()):
            first_tag = token.tag.all()[0]
            token.selected_tag = first_tag
            token.checked = True
            token.save()
          else:
            JsonResponse(response)
        else:
          JsonResponse(response)
          
  response = {
    'type': 'ok',
  }
  return JsonResponse(response)

def token_submit_word(request, word_pos):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  if not request.POST.get('biblg') or not request.POST.get('sentence') or not request.POST.get('token') or not str(word_pos):
    response['response'] = 'Lost data.'
    return JsonResponse(response)
  
  try:
    biblg = Bibliography.objects.get(id=request.POST.get('biblg'))
  except Exception:
    response['response'] = 'Bibliography not found'
    return JsonResponse(response)

  if hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
  
  for text in texts:
    snt = Sentence.objects.filter(text=text).filter(position=request.POST.get('sentence')).order_by('position')
    if len(snt):
      token = Token.objects.filter(sentence=snt[0]).filter(position=request.POST.get('token'))
      if token: 
        token = token[0]
        try:
          tag = token.tag.all()[int(word_pos)]
        except:
          response['response'] = 'Tag not found'
          return JsonResponse(response)
        else:
          if token.selected_tag != tag:
            token.selected_tag = tag
            token.checked = True
            token.save()
            act = 'submit'
          else:
            token.selected_tag = None
            token.checked = False
            token.save()
            act = 'drop'
      else:
        response['response'] = 'Token not found'
        return JsonResponse(response)
    else:
      response['response'] = 'Sentence not found'
      return JsonResponse(response)
          
  response = {
    'type': 'ok',
    'response': 'Success',
    'act': act,
  }
  return JsonResponse(response)

def new_word(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  if not request.POST.get('word') or not request.POST.get('tpl'):
    response['response'] = 'Lost data.'
    return JsonResponse(response)
    
  word = request.POST.get('word')
  tpl = request.POST.get('tpl')
  
  if tpl[:4] == 'conj':
    try:
      p = VerbParser('{tpl}|{root}'.format(tpl=tpl,root=request.POST.get('verb_root')), word)
      p.parse()
    except Exception as E:
      response['response'] = '{}'.format(E)
      return JsonResponse(response)
    else:
      response = {
        'type': 'ok',
        'response': 'Success',
      }
      return JsonResponse(response)
  elif tpl[:7] == 'hy-noun':
    a_on = '|a=on' if request.POST.get('noun_a') else ''
    pl_on = '|pl=on' if request.POST.get('noun_pl') else ''
    unc_on = '|unc=on' if request.POST.get('noun_unc') else ''
    n_on = '|n=on' if request.POST.get('noun_n') else ''
    obl_stem = '||{}'.format(request.POST.get('noun_o_stem')) if request.POST.get('noun_o_stem') else ''
    sing_stem = '||||{}'.format(request.POST.get('noun_s_stem')) if request.POST.get('noun_s_stem') else ''
    tpl = ''.join(['{{', tpl, a_on, pl_on, unc_on, n_on, obl_stem, sing_stem, '}}'])
    try:
      p = NounParserFactory.parser(word, tpl)
      p.save()
    except Exception as E:
      return JsonResponse(response)
    else:
      response = {
        'type': 'ok',
        'response': 'Success',
      }
      return JsonResponse(response)
    
def word_overview(request):
  response = {
    'type': 'error',
    'response': "Սխալմունք",
  }
  
  if request.method != 'POST':
    response['response'] = 'Օգտագործեք \'post\' մեթոդը'
    return JsonResponse(response)
  
  if not request.user.is_authenticated or not request.user.is_active:
    response['response'] = 'Գրանցված չեք'
    return JsonResponse(response)
  
  if not request.POST.get('word') or not request.POST.get('tpl'):
    response['response'] = 'Lost data.'
    return JsonResponse(response)
    
  word = request.POST.get('word')
  tpl = request.POST.get('tpl')
  
  if tpl[:4] == 'conj':
    response = {
      'type': 'ok',
      'response': 'Success',
      'output': '<p>Verb</p>'
    }
    return JsonResponse(response)
  elif tpl[:7] == 'hy-noun':
    a_on = '|a=on' if request.POST.get('noun_a') else ''
    pl_on = '|pl=on' if request.POST.get('noun_pl') else ''
    unc_on = '|unc=on' if request.POST.get('noun_unc') else ''
    n_on = '|n=on' if request.POST.get('noun_n') else ''
    obl_stem = '||{}'.format(request.POST.get('noun_o_stem')) if request.POST.get('noun_o_stem') else ''
    sing_stem = '||||{}'.format(request.POST.get('noun_s_stem')) if request.POST.get('noun_s_stem') else ''
    tpl = ''.join(['{{', tpl, a_on, pl_on, unc_on, n_on, obl_stem, sing_stem, '}}'])
    try:
      p = NounParserFactory.parser(word, tpl)
      output = p.parse_html()
    except Exception as E:
      response['response'] = '{}'.format(E)
      return JsonResponse(response)
    else:
      response = {
        'type': 'ok',
        'response': 'Success',
        'output': output,
      }
      return JsonResponse(response)