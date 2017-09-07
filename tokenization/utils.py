from bibliography.models import Bibliography, Text
from .models import Sentence, Token, Word

def st_count_all():
  response = {
    'tokens': 0,
    'tags': 0,
    'checked_tags': 0,
  }

  biblgs = Bibliography.objects.all()
  for biblg in biblgs:
    if hasattr(biblg, 'press'):
      texts = [biblg.press.text]
    elif hasattr(biblg, 'textbook'):
      texts = biblg.textbook.texts.all()
    elif hasattr(biblg, 'fiction'):
      texts = [biblg.fiction.text]
    
    for text in texts:
      sentences = Sentence.objects.filter(text=text).order_by('position')
      for s in sentences:
        words = Token.objects.filter(sentence=s).order_by('position')
        for w in words:
          response['tokens'] += 1
          if len(w.tag.all()):
            response['tags'] += 1
            if w.checked:
              response['checked_tags'] += 1
              
  return response
  
def st_count_biblg(biblg):
  response = {
    'tokens': 0,
    'tags': 0,
    'checked_tags': 0,
    'sentence': {}
  }
  
  if hasattr(biblg, 'press'):
    texts = [biblg.press.text]
  elif hasattr(biblg, 'textbook'):
    texts = biblg.textbook.texts.all()
  elif hasattr(biblg, 'fiction'):
    texts = [biblg.fiction.text]
  
  for text in texts:
    sentences = Sentence.objects.filter(text=text).order_by('position')
    for s in sentences:
      response['sentence'].update({
        s.position: {
          'tokens': 0,
          'tags': 0,
          'checked_tags': 0,
        }
      })
      words = Token.objects.filter(sentence=s).order_by('id')
      for w in words:
        response['tokens'] += 1
        response['sentence'][s.position]['tokens'] += 1
        if len(w.tag.all()):
          response['tags'] += 1
          response['sentence'][s.position]['tags'] += 1
          if w.checked:
            response['checked_tags'] += 1
            response['sentence'][s.position]['checked_tags'] += 1
              
  return response