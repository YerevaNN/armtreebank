from bibliography.models import Bibliography, Text
from .models import *

from parsers.parser_default import DefaultParser
from parsers.parser_noun import NounParserFactory
from parsers.parser_verb import VerbParserFactory
from parsers.parser_num import NumParser
from parsers.parser_intj import IntjParser
from parsers.parser_pron import PronParser
from parsers.parser_adj import AdjParser
from parsers.parser_adv import AdvParser
from parsers.parser_adp import AdpParser
from parsers.parser_det import DetParser
from parsers.parser_sconj import SconjParser
from parsers.parser_cconj import CconjParser
from parsers.parser_part import PartParser
from parsers.parser_aux import AuxParser
from parsers.parser_punct import PunctParser
from parsers.parser_sym import SymParser
from parsers.parser_x import XParser

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

def get_parser(tpl, form):
  if tpl == 'noun':
    parser = NounParserFactory.parser(form.get('noun_tpl'))()
  elif tpl == 'verb':
    parser = VerbParserFactory.parser(form.get('verb_tpl'))()
  elif tpl == 'sconj':
    parser = SconjParser()
  elif tpl == 'cconj':
    parser = CconjParser()
  elif tpl == 'part':
    parser = PartParser()
  elif tpl == 'aux':
    parser = AuxParser()
  elif tpl == 'punct':
    parser = PunctParser()
  elif tpl == 'sym':
    parser = SymParser()
  elif tpl == 'x':
    parser = XParser()
  elif tpl == 'num':
    parser = NumParser()
  elif tpl == 'intj':
    parser = IntjParser()
  elif tpl == 'pron':
    parser = PronParser()
  elif tpl == 'adj':
    parser = AdjParser()
  elif tpl == 'adv':
    parser = AdvParser()
  elif tpl == 'adp':
    parser = AdpParser()
  elif tpl == 'det':
    parser = DetParser()

  return parser

def extract_ud_features( instance ):
  features = []
  for feat, val in instance.__dict__.items():
    if feat == 'id' or feat == 'parent_id' or feat == 'voice' or \
       feat == 'value_sym' or feat == 'nominalized' or feat == 'proper' or \
       feat[0] == '_' or feat == 'lemma':
      continue

    if (val or val == 0) and (val is not False and val != 'False'):
      name = feat if feat != 'voice_feat' else 'voice'
      feat_name = ''.join(' '.join(name.split('_')).title().split())
      features.append('='.join([feat_name, str(val).title()]))

  return '|'.join(sorted(features)) if features else '_'