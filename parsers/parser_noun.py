import os

import re
import csv

from collections import OrderedDict

from tokenization.models import Word, Noun, NounAnimacy
from tokenization.forms import NounSaveForm

class NounManualParser:
  def data_from_request(self, request):
    self.form = NounSaveForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'noun'
    wrd.save()
    if self.form.is_valid():
      noun = self.form.save()
      noun.parent = wrd
      noun.save()
  
  def parse_html(self):
    return '{}'.format('noun'.upper())

class NounParser:
  declensions = OrderedDict([
    ('nominative-singular', 'NS'),
    ('nominative-plural', 'NP'),
    ('dative-singular', 'DS'),
    ('dative-plural', 'DP'),
    ('ablative-singular', 'AS'),
    ('ablative-plural', 'AP'),
    ('instrumental-singular', 'IS'),
    ('instrumental-plural', 'IP'),
    ('locative-singular', 'LS'),
    ('locative-plural', 'LP'),
    ('nominative-singular-definite', 'NSD'),
    ('nominative-plural-definite', 'NPD'),
    ('dative-singular-definite', 'DSD'),
    ('dative-plural-definite', 'DPD'),
    ('nominative-singular-first', 'NSF'),
    ('nominative-plural-first', 'NPF'),
    ('dative-singular-first', 'DSF'),
    ('dative-plural-first', 'DPF'),
    ('ablative-singular-first', 'ASF'),
    ('ablative-plural-first', 'APF'),
    ('instrumental-singular-first', 'ISF'),
    ('instrumental-plural-first', 'IPF'),
    ('locative-singular-first', 'LSF'),
    ('locative-plural-first', 'LPF'),
    ('nominative-singular-second', 'NSS'),
    ('nominative-plural-second', 'NPS'),
    ('dative-singular-second', 'DSS'),
    ('dative-plural-second', 'DPS'),
    ('ablative-singular-second', 'ASS'),
    ('ablative-plural-second', 'APS'),
    ('instrumental-singular-second', 'ISS'),
    ('instrumental-plural-second', 'IPS'),
    ('locative-singular-second', 'LSS'),
    ('locative-plural-second', 'LPS'),
  ])
  
  def parse_word( self, type ):
    return (
      '-'.join(self.attr[0][1].split('-')[2:4]),
      self.declensions.get(type),
      type,
      {
        'oblique-stem': self.word if not self.word_attr(2) else self.word_attr(2),
        'singular-stem': self.word if not self.word_attr(4) else self.word_attr(4),
        'word': getattr(self, self.declensions.get(type))(),
      },
      {
        'animate': True if self.word_attr_k('a=on') else False,
        'inanimate': True if self.word_attr_k('ia=on') else False,
        'human': True if self.word_attr_k('hum=on') else False,
        'uncountable': True if self.word_attr_k('unc=on') else False,
        'plural_only': True if self.word_attr_k('pl=on') else False,
        'nominalized': True if self.word_attr_k('n=on') else False,
        'proper': True if self.word_attr_k('propn=on') else False,
        'concrete': True if self.word_attr_k('conc=on') else False,
        'abstract': True if self.word_attr_k('astr=on') else False,
      },
    )
  
  def parse( self, type=False ):
    if type:
      if not self.declensions.get(type):
        raise KeyError
      else:
        return self.parse_word( type )
    else:
      d_arr = []
      for d in self.declensions:
        d_arr.append(self.parse_word( d ))
      return d_arr
      
  def save( self ):
    output = self.parse()
    for i in output:
      if i[3]['word'] and i[3]['word'] != '-':
        if not isinstance(i[3]['word'], list):
          i[3]['word'] = [i[3]['word']]
        for j in range(len(i[3]['word'])):
          wrd = Word()
          wrd.pos = 'noun'
          wrd.word = i[3]['word'][j]
          wrd.save()
          noun = Noun()
          noun.parent = wrd
          noun.lemma = self.word
          #noun.oblique_stem = i[3]['oblique-stem']
          #noun.singular_stem = i[3]['singular-stem']
          #noun.declension_type = i[0].split('-')[0]
          noun.case = i[2].split('-')[0][:3]
          #noun.quantity_type = 'ներ' if i[0].split('-')[-1] == 'ներ' else ( 'եր' if not i[4]['plural_only'] else '-' )
          if i[4]['uncountable']:
            noun.number = 'coll' 
          elif i[4]['plural_only']:
            noun.number = 'assoc'
          else:
            noun.number = i[2].split('-')[1][:4]
          noun.nominalized = i[4]['nominalized']
          noun.proper = i[4]['proper']
          noun.materiality = 'conc' if i[4]['concrete'] else 'astr'
          noun.poss_number = 'sing'
          if len(i[1]) != 2:
            noun.poss_person = '1' if i[1][-1] == 'F' else ( '2' if i[1][-1] == 'S' else '3' )
          noun.save()
          if i[4]['animate']:
            noun.animacy.add(NounAnimacy.objects.get(value='animate'))
          if i[4]['inanimate']:
            noun.animacy.add(NounAnimacy.objects.get(value='inanimate'))
          if i[4]['human']:
            noun.animacy.add(NounAnimacy.objects.get(value='human'))
          noun.save()
          if len(i[1]) != 2:
            noun.definite = 'def'
          else:
            noun.definite = 'indef'
          try:
            noun.verb_form = self.extra_features.get('verb_form') or ''
            noun.name_type = self.extra_features.get('name_type') or ''
          except:
            pass
          noun.save()
              
  def html_base( self ):
    return '\
    <html>\
      <head>\
        <meta charset="utf-8">\
      </head>\
      <body>\
        <h2>{header}</h2>\
        {table}\
      </body>\
    </html>'
  
  def parse_html( self, base=False ):
    html = '<table class="ui celled grey inverted table" style="font-size: 12px;">\
      <thead>\
        <tr>\
          <th>NS</th>\
          <th>NP</th>\
          <th>DS</th>\
          <th>DP</th>\
          <th>AS</th>\
          <th>AP</th>\
          <th>IS</th>\
          <th>IP</th>\
          <th>LS</th>\
          <th>LP</th>\
        </tr>\
      </thead>\
      <tbody>'

    for d in self.declensions:
      if self.declensions.get(d)[:2] == 'NS':
        html += '<tr>'

      html += '<td>{}</td>'.format(getattr(self, self.declensions.get(d))())

      if self.declensions.get(d)[:2] == 'LP' or self.declensions.get(d) == 'DPD':
        html += '</tr>'

    html += '</tbody></table>'
    return self.html_base().format(table=html, header='{w} {a}'.format(w=self.word,a=self.not_parsed_attr)) if base else html
  
  def data( self, word, attr, **kwargs ):
    self.not_parsed_attr = attr
    self.word = word
    attr_list = re.split(r'\|(?=\|*)', attr[2:-2])
    for i in range(len(attr_list)-1, -1, -1):
      if attr_list[i] == '':
        attr_list[i+1] = '|' + attr_list[i+1]
        del attr_list[i]
    for i in range(len(attr_list)):
      attr_list[i] = '|' + attr_list[i]
    attributes = []
    for i in attr_list:
      attributes.append((i.count('|'), re.sub( r'\|', '', i)))
    self.attr = attributes

  def data_from_request(self, request):
    n_on = '|n=on' if request.POST.get('nominalized') else ''
    proper = '|propn=on' if request.POST.get('proper') else ''
    obl_stem = '||{}'.format(request.POST.get('parser_o_stem')) if request.POST.get('parser_o_stem') else ''
    sing_stem = '||||{}'.format(request.POST.get('parser_s_stem')) if request.POST.get('parser_s_stem') else ''
    pl_on = '|pl=on' if request.POST.get('parser_number') == 'assocpl' else ''
    unc_on = '|unc=on' if request.POST.get('parser_number') == 'col' else ''
    a_on = '|a=on' if 'anim' in request.POST.getlist('animacy') else ''
    ia_on = '|ia=on' if 'inan' in request.POST.getlist('animacy') else ''
    h_on = '|hum=on' if 'human' in request.POST.getlist('animacy') else ''
    conc_on = '|conc=on' if request.POST.get('materiality') == 'conc' else ''
    astr_on = '|astr=on' if request.POST.get('materiality') == 'astr' else ''
    self.extra_features = {
      'name_type': request.POST.get('name_type'),
      'verb_form': request.POST.get('verb_form'),
    }
    
    tpl = request.POST.get('tpl')
    word = request.POST.get('word')

    tpl = ''.join(['{{', tpl, n_on, proper, obl_stem, sing_stem, pl_on, unc_on, a_on, ia_on, h_on, conc_on, astr_on, '}}'])
    
    self.data(word, tpl)

  @staticmethod   
  def vowend( word ):
    vowels = ['ա', 'ե', 'է', 'ի', 'ո', 'օ']
    if word[-1] in vowels or word[-2:] == 'ու':
      return '{}ն'.format(word)
    else:
      return ['{}ն'.format(word), '{}ը'.format(word)]
  
  @staticmethod
  def glide( word ):
    vowels = ['ա', 'ո', 'օ']
    if word[-1] in vowels:
      return '{}յ'.format(word)
    else:
      return '{}'.format(word)
  
  @staticmethod
  def utyun( word ):
    return word[:-7]
    
  @staticmethod
  def utiwn( word ):
    return word[:-6]
    
  @staticmethod
  def i( word ):
    if word[-1] == 'ի':
      return word[:-1]
    else:
      return word
      
  def word_attr( self, attr ):
    for u, v in self.attr:
      if u == attr:
        return v
    return ''
    
  def word_attr_k( self, attr ):
    for u, v in self.attr:
      if v == attr:
        return True
    return False
    
  def NS( self ):
    raise NotImplementedError
    
  def NP( self ):
    raise NotImplementedError
    
  def DS( self ):
    raise NotImplementedError
    
  def DP( self ):
    raise NotImplementedError
    
  def AS( self ):
    raise NotImplementedError
    
  def AP( self ):
    raise NotImplementedError
    
  def IS( self ):
    raise NotImplementedError
    
  def IP( self ):
    raise NotImplementedError
    
  def LS( self ):
    raise NotImplementedError
    
  def LP( self ):
    raise NotImplementedError
    
  def NSD( self ):
    raise NotImplementedError
    
  def NPD( self ):
    raise NotImplementedError
    
  def DSD( self ):
    raise NotImplementedError
    
  def DPD( self ):
    raise NotImplementedError
    
  def NSF( self ):
    raise NotImplementedError
    
  def NPF( self ):
    raise NotImplementedError
    
  def DSF( self ):
    raise NotImplementedError
    
  def DPF( self ):
    raise NotImplementedError
    
  def ASF( self ):
    raise NotImplementedError
    
  def APF( self ):
    raise NotImplementedError
    
  def ISF( self ):
    raise NotImplementedError
    
  def IPF( self ):
    raise NotImplementedError
    
  def LSF( self ):
    raise NotImplementedError
    
  def LPF( self ):
    raise NotImplementedError
    
  def NSS( self ):
    raise NotImplementedError
    
  def NPS( self ):
    raise NotImplementedError
    
  def DSS( self ):
    raise NotImplementedError
    
  def DPS( self ):
    raise NotImplementedError
    
  def ASS( self ):
    raise NotImplementedError
    
  def APS( self ):
    raise NotImplementedError
    
  def ISS( self ):
    raise NotImplementedError
    
  def IPS( self ):
    raise NotImplementedError
    
  def LSS( self ):
    raise NotImplementedError
    
  def LPS( self ):
    raise NotImplementedError
    
class NounINerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ի'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ի'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ի'.format(self.glide(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ից'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ից'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ից'.format(self.glide(self.word))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ով'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ով'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ով'.format(self.glide(self.word))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ում'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ում'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ում'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներում'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ներում'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ները'.format(self.word_attr(4) if self.word_attr(4) else self.word), 
        '{}ներն'.format(self.word_attr(4) if self.word_attr(4) else self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ին'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ին'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ին'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իս'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իցս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իցս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իցս'.format(self.glide(self.word))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ովս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ովս'.format(self.glide(self.word))
    else:
      return '-'
    
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումս'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ումս'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ումս'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներումս'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ներումս'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իդ'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իցդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իցդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իցս'.format(self.glide(self.word))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ովդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ովդ'.format(self.glide(self.word))
    else:
      return '-'
    
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումդ'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ումդ'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ումդ'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներումդ'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ներումդ'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
      
class NounIErParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}եր'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ի'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ի'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ի'.format(self.glide(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երի'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ից'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ից'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ից'.format(self.glide(self.word))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երից'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ով'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ով'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ով'.format(self.glide(self.word))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երով'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ում'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ում'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ում'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}երում'.format(self.glide(self.word_attr(4)))
        else:
          return '{}երում'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}երը'.format(self.word_attr(4) if self.word_attr(4) else self.word), 
        '{}երն'.format(self.word_attr(4) if self.word_attr(4) else self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ին'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ին'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ին'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երին'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իս'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իցս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իցս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իցս'.format(self.glide(self.word))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովս'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ովս'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ովս'.format(self.glide(self.word))
    else:
      return '-'
    
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումս'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ումս'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ումս'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}երումս'.format(self.glide(self.word_attr(4)))
        else:
          return '{}երումս'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իդ'.format(self.glide(self.word))
    else:
      return '-'
    
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}իցդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}իցդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}իցս'.format(self.glide(self.word))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովդ'.format(self.word_attr(2))
      elif self.word_attr(4):
        return '{}ովդ'.format(self.glide(self.word_attr(4)))
      else:
        return '{}ովդ'.format(self.glide(self.word))
    else:
      return '-'
    
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումդ'.format(self.word_attr(2))
        elif self.word_attr(4):
          return '{}ումդ'.format(self.glide(self.word_attr(4)))
        else:
          return '{}ումդ'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}երումդ'.format(self.glide(self.word_attr(4)))
        else:
          return '{}երումդ'.format(self.glide(self.word))
      else:
        return '-'
    else:
      return '-'
      
class NounUtyunParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ության'.format(self.utyun(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ների'.format(self.word), '{}ությանց'.format(self.utyun(self.word))]
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ից'.format(self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ությամբ'.format(self.utyun(self.word)), '{}ով'.format(self.word)]
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ը'.format(self.word), '{}ն'.format(self.word)]
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ները'.format(self.word), '{}ներն'.format(self.word)]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ությանը'.format(self.utyun(self.word)), '{}ությանն'.format(self.utyun(self.word))]
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
    
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
      
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ությանս'.format(self.utyun(self.word))
    else:
      return '-'
    
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ներիս'.format(self.word), '{}ությանցս'.format(self.utyun(self.word))]
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցս'.format(self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ովս'.format(self.word), '{}ությամբս'.format(self.utyun(self.word))]
    else:
      return '-'
    
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
    
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
      
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ությանդ'.format(self.utyun(self.word))
    else:
      return '-'
    
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ներիդ'.format(self.word), '{}ությանցդ'.format(self.utyun(self.word))]
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցդ'.format(self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ովդ'.format(self.word), '{}ությամբդ'.format(self.utyun(self.word))]
    else:
      return '-'
    
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
class NounUNerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ու'.format(self.i(self.word_attr(2)))
      else:
        return '{}ու'.format(self.i(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուց'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուց'.format(self.i(self.word))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ով'.format(self.i(self.word_attr(2)))
      else:
        return '{}ով'.format(self.i(self.word))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ում'.format(self.i(self.word_attr(2)))
        else:
          return '{}ում'.format(self.i(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներում'.format(self.i(self.word_attr(4)))
        else:
          return '{}ներում'.format(self.i(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ն'.format(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ները'.format(self.word_attr(4) if self.word_attr(4) else self.word), 
        '{}ներն'.format(self.word_attr(4) if self.word_attr(4) else self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուն'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուն'.format(self.i(self.word))
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
    
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուս'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուս'.format(self.i(self.word))
    else:
      return '-'
    
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուցս'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուցս'.format(self.i(self.word))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովս'.format(self.i(self.word_attr(2)))
      else:
        return '{}ովս'.format(self.i(self.word))
    else:
      return '-'
    
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումս'.format(self.i(self.word_attr(2)))
        else:
          return '{}ումս'.format(self.i(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներումս'.format(self.word_attr(4))
        else:
          return '{}ներումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
    
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուդ'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուդ'.format(self.i(self.word))
    else:
      return '-'
    
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ուցդ'.format(self.i(self.word_attr(2)))
      else:
        return '{}ուցդ'.format(self.i(self.word))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}ովդ'.format(self.i(self.word_attr(2)))
      else:
        return '{}ովդ'.format(self.i(self.word))
    else:
      return '-'
    
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word_attr(4) if self.word_attr(4) else self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(2):
          return '{}ումդ'.format(self.i(self.word_attr(2)))
        else:
          return '{}ումդ'.format(self.i(self.word))
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ներումդ'.format(self.word_attr(4))
        else:
          return '{}ներումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
class NounANerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ա'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անից'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return [ '{}ը'.format(self.word), '{}ն'.format(self.word) ]
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ները'.format(self.word), 
        '{}ներն'.format(self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ան'.format(self.word_attr(2))
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word)
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անիցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անիցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}անովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounAnNerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return [
          '{}ան'.format(self.word_attr(2)),
          '{}ի'.format(self.word_attr(4)),
        ]
      else:
        return [
          '{}ան'.format(self.word_attr(2)),
          '{}ի'.format(self.word),
        ]
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ից'.format(self.word_attr(4))
      else:
        return '{}ից'.format(self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return [
          '{}ամբ'.format(self.word_attr(2)),
          '{}ով'.format(self.word_attr(4)),
        ]
      else:
        return [
          '{}ամբ'.format(self.word_attr(2)),
          '{}ով'.format(self.word),
        ]
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ում'.format(self.word_attr(4))
        else:
          return '{}ում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ները'.format(self.word), 
        '{}ներն'.format(self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return [
          '{}անը'.format(self.word_attr(2)),
          '{}անն'.format(self.word_attr(2)),
          '{}ին'.format(self.word_attr(4)),
        ]
      else:
        return [
          '{}անը'.format(self.word_attr(2)),
          '{}անն'.format(self.word_attr(2)),
          '{}ին'.format(self.word),
        ]
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return [
          '{}անս'.format(self.word_attr(2)),
          '{}իս'.format(self.word_attr(4)),
        ]
      else:
        return [
          '{}անս'.format(self.word_attr(2)),
          '{}իս'.format(self.word),
        ]
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}իցս'.format(self.word_attr(4))
      else:
        return '{}իցս'.format(self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովս'.format(self.word_attr(4))
      else:
        return '{}ովս'.format(self.word)
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումս'.format(self.word_attr(4))
        else:
          return '{}ումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'      
      
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return [
          '{}անդ'.format(self.word_attr(2)),
          '{}իդ'.format(self.word_attr(4)),
        ]
      else:
        return [
          '{}անդ'.format(self.word_attr(2)),
          '{}իդ'.format(self.word),
        ]
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}իցդ'.format(self.word_attr(4))
      else:
        return '{}իցդ'.format(self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովդ'.format(self.word_attr(4))
      else:
        return '{}ովդ'.format(self.word)
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումդ'.format(self.word_attr(4))
        else:
          return '{}ումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'

class NounUtionParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ութեան'.format(self.utiwn(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ների'.format(self.word), '{}ութեանց'.format(self.utiwn(self.word))]
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ից'.format(self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ութեամբ'.format(self.utiwn(self.word)), '{}ով'.format(self.word)]
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ը'.format(self.word), '{}ն'.format(self.word)]
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ները'.format(self.word), '{}ներն'.format(self.word)]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ութեանը'.format(self.utiwn(self.word)), '{}ութեանն'.format(self.utiwn(self.word))]
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word)
    else:
      return '-'
      
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
    
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
      
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ութեանս'.format(self.utiwn(self.word))
    else:
      return '-'
    
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ներիս'.format(self.word), '{}ութեանցս'.format(self.utiwn(self.word))]
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցս'.format(self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ովս'.format(self.word), '{}ութեամբս'.format(self.utiwn(self.word))]
    else:
      return '-'
    
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
    
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
      
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ութեանդ'.format(self.utiwn(self.word))
    else:
      return '-'
    
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return ['{}ներիդ'.format(self.word), '{}ութեանցդ'.format(self.utiwn(self.word))]
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցդ'.format(self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return ['{}ովդ'.format(self.word), '{}ութեամբդ'.format(self.utiwn(self.word))]
    else:
      return '-'
    
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
class NounOjErParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}եր'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երի'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջից'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջով'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word), 
        '{}ն'.format(self.word),
      ]
    else:
      return '-'
      
  def NPD( self ):
    if not self.word_attr_k('pl=on'):
      return [ 
        '{}երը'.format(self.word), 
        '{}երն'.format(self.word),
      ]
    else:
      return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ոջը'.format(self.word_attr(2) if self.word_attr(2) else self.word), 
        '{}ոջն'.format(self.word_attr(2) if self.word_attr(2) else self.word),
      ]
    else:
      return '-'
      
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երին'.format(self.word),
    else:
      return '-'

  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounOjNerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջից'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջով'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word), 
        '{}ն'.format(self.word),
      ]
    else:
      return '-'
      
  def NPD( self ):
    if not self.word_attr_k('pl=on'):
      return [ 
        '{}ները'.format(self.word), 
        '{}ներն'.format(self.word),
      ]
    else:
      return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ոջը'.format(self.word_attr(2) if self.word_attr(2) else self.word), 
        '{}ոջն'.format(self.word_attr(2) if self.word_attr(2) else self.word),
      ]
    else:
      return '-'
      
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word),
    else:
      return '-'

  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounVorErParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}եր'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երի'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ից'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word), 
        '{}ն'.format(self.word),
      ]
    else:
      return '-'
      
  def NPD( self ):
    if not self.word_attr_k('pl=on'):
      return [ 
        '{}երը'.format(self.word), 
        '{}երն'.format(self.word),
      ]
    else:
      return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word_attr(2)), 
        '{}ն'.format(self.word_attr(2)),
      ]
    else:
      return '-'
      
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երին'.format(self.word),
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounVorNerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ից'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word), 
        '{}ն'.format(self.word),
      ]
    else:
      return '-'
      
  def NPD( self ):
    if not self.word_attr_k('pl=on'):
      return [ 
        '{}ները'.format(self.word), 
        '{}ներն'.format(self.word),
      ]
    else:
      return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word_attr(2)), 
        '{}ն'.format(self.word_attr(2)),
      ]
    else:
      return '-'
      
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word),
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
  
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}իցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounVaNerParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներ'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վա'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ների'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանից'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ով'.format(self.word_attr(4))
      else:
        return '{}ով'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ում'.format(self.word_attr(4))
        else:
          return '{}ում'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ները'.format(self.word), 
        '{}ներն'.format(self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}վան'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներին'.format(self.word)
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վաս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանիցս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովս'.format(self.word_attr(4))
      else:
        return '{}ովս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումս'.format(self.word_attr(4))
        else:
          return '{}ումս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վադ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանիցդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովդ'.format(self.word_attr(4))
      else:
        return '{}ովդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ներովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումդ'.format(self.word_attr(4))
        else:
          return '{}ումդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}ներումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
class NounVaErParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}եր'.format(self.word)
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վա'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երի'.format(self.word)
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանից'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երից'.format(self.word)
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ով'.format(self.word_attr(4))
      else:
        return '{}ով'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երով'.format(self.word)
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ում'.format(self.word_attr(4))
        else:
          return '{}ում'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երում'.format(self.word)
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word)
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}երը'.format(self.word), 
        '{}երն'.format(self.word),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(2):
        return '{}վան'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երին'.format(self.word)
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երս'.format(self.word)
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վաս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիս'.format(self.word)
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանիցս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցս'.format(self.word)
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովս'.format(self.word_attr(4))
      else:
        return '{}ովս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովս'.format(self.word)
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումս'.format(self.word_attr(4))
        else:
          return '{}ումս'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երումս'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երդ'.format(self.word)
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վադ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիդ'.format(self.word)
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}վանիցդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցդ'.format(self.word)
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      if self.word_attr(4):
        return '{}ովդ'.format(self.word_attr(4))
      else:
        return '{}ովդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովդ'.format(self.word)
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        if self.word_attr(4):
          return '{}ումդ'.format(self.word_attr(4))
        else:
          return '{}ումդ'.format(self.word_attr(2) if self.word_attr(2) else self.word)
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երումդ'.format(self.word)
      else:
        return '-'
    else:
      return '-'
      
class NounOjAyqParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}այք'.format(self.word_attr(4))
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անց'.format(self.word_attr(4))
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջից'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցից'.format(self.word_attr(4))
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցով'.format(self.word_attr(4))
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ը'.format(self.word), 
        '{}ն'.format(self.word),
      ]
    else:
      return '-'
      
  def NPD( self ):
    return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}ոջը'.format(self.word_attr(2)), 
        '{}ոջն'.format(self.word_attr(2)),
      ]
    else:
      return '-'
      
  def DPD( self ):
    return '-'
    
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}այքս'.format(self.word_attr(4))
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցս'.format(self.word_attr(4))
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցիցս'.format(self.word_attr(4))
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցովս'.format(self.word_attr(4))
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}այքդ'.format(self.word_attr(4))
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցդ'.format(self.word_attr(4))
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջիցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցիցդ'.format(self.word_attr(4))
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ոջովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}անցովդ'.format(self.word_attr(4))
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounUIqParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return [
        '{}իներ'.format(self.i(self.word)),
        '{}իք'.format(self.i(self.word)),
      ]
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ու'.format(self.i(self.word))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return [
        '{}իների'.format(self.i(self.word)),
        '{}ոց'.format(self.i(self.word)),
      ]
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուց'.format(self.i(self.word))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներից'.format(self.i(self.word))
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ով'.format(self.i(self.word))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներով'.format(self.i(self.word))
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ին'.format(self.i(self.word))
    else:
      return '-'
      
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}իները'.format(self.i(self.word)), 
        '{}իներն'.format(self.i(self.word)),
      ]
    else:
      return '-'
    
  def DSD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ուն'.format(self.i(self.word))
    else:
      return '-'
      
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներին'.format(self.i(self.word))
    else:
      return '-'
    
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.i(self.word))
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներս'.format(self.i(self.word))
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուս'.format(self.i(self.word))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}ունս'.format(self.i(self.word))
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցս'.format(self.i(self.word))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներիցս'.format(self.i(self.word))
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովս'.format(self.i(self.word))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներովս'.format(self.i(self.word))
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.i(self.word))
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներդ'.format(self.i(self.word))
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուդ'.format(self.i(self.word))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներիդ'.format(self.i(self.word))
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցդ'.format(self.i(self.word))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներիցդ'.format(self.i(self.word))
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովդ'.format(self.i(self.word))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իներովդ'.format(self.i(self.word))
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
      
class NounUErParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}եր'.format(self.word_attr(2))
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ու'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երի'.format(self.word_attr(2))
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուց'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երից'.format(self.word_attr(2))
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երով'.format(self.word_attr(2))
    else:
      return '-'
      
  def LS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ում'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'
    
  def LP( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երում'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word_attr(2))
    else:
      return '-'
    
  def NPD( self ):
    if not self.word_attr_k('unc=on'):
      return [ 
        '{}երը'.format(self.word_attr(2)), 
        '{}երն'.format(self.word_attr(2)),
      ]
    else:
      return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուն'.format(self.word_attr(2))
    else:
      return '-'
    
  def DPD( self ):
    if not self.word_attr_k('unc=on'):
        return '{}երին'.format(self.word_attr(2))
    else:
      return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երս'.format(self.word_attr(2))
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիս'.format(self.word_attr(2))
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def LSF( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումս'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'
    
  def LPF( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երումս'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'
      
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}դ'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երդ'.format(self.word_attr(2))
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երիցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}երովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def LSS( self ):
    if not self.word_attr_k('pl=on'):
      if not self.word_attr_k('a=on'):
        return '{}ումդ'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'
    
  def LPS( self ):
    if not self.word_attr_k('unc=on'):
      if not self.word_attr_k('a=on'):
        return '{}երումդ'.format(self.word_attr(2))
      else:
        return '-'
    else:
      return '-'

class NounUIkParser(NounParser):
  def NS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իկ'.format(self.word_attr(2))
    else:
      return '-'
    
  def DS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ու'.format(self.word_attr(2))
    else:
      return '-'
      
  def DP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանց'.format(self.word_attr(2))
    else:
      return '-'
      
  def AS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուց'.format(self.word_attr(2))
    else:
      return '-'
      
  def AP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցից'.format(self.word_attr(2))
    else:
      return '-'
      
  def IS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ով'.format(self.word_attr(2))
    else:
      return '-'
      
  def IP( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցով'.format(self.word_attr(2))
    else:
      return '-'
      
  def LS( self ):
    return '-'
    
  def LP( self ):
    return '-'
    
  def NSD( self ):
    if not self.word_attr_k('pl=on'):
      return self.vowend(self.word_attr(2))
    else:
      return '-'
    
  def NPD( self ):
    return '-'
      
  def DSD( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուն'.format(self.word_attr(2))
    else:
      return '-'
    
  def DPD( self ):
    return '-'
  
  def NSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ս'.format(self.word)
    else:
      return '-'
      
  def NPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իկս'.format(self.word_attr(2))
    else:
      return '-'
    
  def DSF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուս'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def ASF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def APF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցիցս'.format(self.word_attr(2))
    else:
      return '-'
      
  def ISF( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPF( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցովս'.format(self.word_attr(2))
    else:
      return '-'
      
  def LSF( self ):
    return '-'
    
  def LPF( self ):
    return '-'
    
  def NSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}'.format(self.word)
    else:
      return '-'
      
  def NPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}իկդ'.format(self.word_attr(2))
    else:
      return '-'
    
  def DSS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def DPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def ASS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ուցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def APS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցիցդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def ISS( self ):
    if not self.word_attr_k('pl=on'):
      return '{}ովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def IPS( self ):
    if not self.word_attr_k('unc=on'):
      return '{}կանցովդ'.format(self.word_attr(2))
    else:
      return '-'
      
  def LSS( self ):
    return '-'
    
  def LPS( self ):
    return '-'
    
class NounParserFactory:
  parsers = {
    'ի-եր' : NounIErParser,
    'ի-ներ' : NounINerParser,
    'ություն' : NounUtyunParser,
    'ութիւն' : NounUtionParser,
    'ու-ներ' : NounUNerParser,
    'ա-ներ' : NounANerParser,
    'ան-ներ' : NounAnNerParser,
    'ոջ-եր' : NounOjErParser,
    'ոջ-ներ' : NounOjNerParser,
    'որ-եր' : NounVorErParser,
    'որ-ներ' : NounVorNerParser,
    'վա-եր' : NounVaErParser,
    'վա-ներ' : NounVaNerParser,
    'ոջ-այք' : NounOjAyqParser,
    'ու-իք' : NounUIqParser,
    'ու-եր' : NounUErParser,
    'ու-իկ' : NounUIkParser,
  }
  
  @classmethod
  def sync( cls, drop=False ):
    if drop:
      i = 0
      for _w in Word.objects.all():
        if len(Noun.objects.filter(parent=_w)):
          _v = Noun.objects.filter(parent=_w)[0]
          _v.delete()
          _w.delete()
          print('Deleted..', i)
          i += 1

    dir_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(dir_path, '../','sync/en_nouns.csv')

    with open(csv_path, 'r+', encoding='utf-8') as in_file:
      csvreader = csv.reader(in_file, delimiter=',')
      n = 0
      for row in csvreader:
        if isinstance(row, list) and len(row) == 2:
          attr = row[1].split('~')
          for a in attr:
            try:
              parser = cls.parser(a)()
              parser.data(row[0], a)
              parser.save()
              n += 1
              print('Saved: ', n)
            except Exception as E:
              print(E)

  @classmethod
  def parser( cls, attr, **kwargs ):
    if attr == 'manual':
      return NounManualParser

    if attr[:2] == '{{':
      attr = attr[2:-2]

    p_type = re.split(r'\|(?=\|*)', attr)[0][8:]

    if not p_type or not cls.parsers.get( p_type ):
      raise KeyError
    else:
      return cls.parsers.get( p_type )

if __name__ == '__main__':
  try:
    parser = NounParserFactory.parser('{{hy-noun-ություն}}')()
    parser.data('ամուսնություն', '{{hy-noun-ություն}}')
    output = parser.parse()
  except Exception as E:
    print(E)
  else:
    file = open('output.txt', 'w', encoding='utf-8')
    file.write(str(output))
    file.close()