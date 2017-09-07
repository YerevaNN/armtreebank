import re

#from .models import Word, Verb

class VerbParser:
  conjugations = {
    'infinitive': '-I',
    'infinitive-caus': '-IC',
    'infinitive-passive': '-IP',
    'infinitive-caus-passive': '-ICP',
    'infinitive-neg': '-IN',
    'infinitive-neg-caus': '-INC',
    'infinitive-neg-passive': '-INP',
    'infinitive-neg-caus-passive': '-INCP',
    'resultative_participle': '-RP',
    'resultative_participle-caus': '-RPC',
    'resultative_participle-passive': '-RPP',
    'resultative_participle-caus-passive': '-RPCP',
    'resultative_participle-neg': '-RPN',
    'resultative_participle-neg-caus': '-RPNC',
    'resultative_participle-neg-passive': '-RPNP',
    'resultative_participle-neg-caus-passive': '-RPNCP',
    'subject_participle': '-SP',
    'subject_participle-caus': '-SPC',
    'subject_participle-passive': '-SPP',
    'subject_participle-caus-passive': '-SPCP',
    'subject_participle-neg': '-SPN',
    'subject_participle-neg-caus': '-SPNC',
    'subject_participle-neg-passive': '-SPNP',
    'subject_participle-neg-caus-passive': '-SPNCP',
    'imperfective_converb': '-IC',
    'imperfective_converb-caus': '-ICC',
    'imperfective_converb-passive': '-ICP',
    'imperfective_converb-caus-passive': '-ICCP',
    'simultaneous_converb': '-SC',
    'simultaneous_converb-caus': '-SCC',
    'simultaneous_converb-passive': '-SCP',
    'simultaneous_converb-caus-passive': '-SCCP',
    'perfective_converb': '-PC',
    'perfective_converb-caus': '-PCC',
    'perfective_converb-passive': '-PCP',
    'perfective_converb-caus-passive': '-PCCP',
    'future_converb-i': '-FCI',
    'future_converb-i-caus': '-FCIC',
    'future_converb-i-passive': '-FCIP',
    'future_converb-i-caus-passive': '-FCICP',
    'future_converb-ii': '-FCII',
    'future_converb-ii-caus': '-FCIIC',
    'future_converb-ii-passive': '-FCIIP',
    'future_converb-ii-caus-passive': '-FCIICP',
    'connegative_converb': '-CC',
    'connegative_converb-caus': '-CCC',
    'connegative_converb-passive': '-CCP',
    'connegative_converb-caus-passive': '-CCCP',
    # +++++++++++++++
    'indicative-aorist-singular-first': '~IASF',
    'indicative-aorist-singular-second': '~IASS',
    'indicative-aorist-singular-third': '~IAST',
    'indicative-aorist-plural-first': '~IAPF',
    'indicative-aorist-plural-second': '~IAPS',
    'indicative-aorist-plural-third': '~IAPT',
    'indicative-aorist-caus-singular-first': '~IACSF',
    'indicative-aorist-caus-singular-second': '~IACSS',
    'indicative-aorist-caus-singular-third': '~IACST',
    'indicative-aorist-caus-plural-first': '~IACPF',
    'indicative-aorist-caus-plural-second': '~IACPS',
    'indicative-aorist-caus-plural-third': '~IACPT',
    'indicative-aorist-passive-singular-first': '~IAPSF',
    'indicative-aorist-passive-singular-second': '~IAPSS',
    'indicative-aorist-passive-singular-third': '~IAPST',
    'indicative-aorist-passive-plural-first': '~IAPPF',
    'indicative-aorist-passive-plural-second': '~IAPPS',
    'indicative-aorist-passive-plural-third': '~IAPPT',
    'indicative-aorist-caus-passive-singular-first': '~IACPSF',
    'indicative-aorist-caus-passive-singular-second': '~IACPSS',
    'indicative-aorist-caus-passive-singular-third': '~IACPST',
    'indicative-aorist-caus-passive-plural-first': '~IACPPF',
    'indicative-aorist-caus-passive-plural-second': '~IACPPS',
    'indicative-aorist-caus-passive-plural-third': '~IACPPT',
    'indicative-aorist-neg-singular-first': '~IANSF',
    'indicative-aorist-neg-singular-second': '~IANSS',
    'indicative-aorist-neg-singular-third': '~IANST',
    'indicative-aorist-neg-plural-first': '~IANPF',
    'indicative-aorist-neg-plural-second': '~IANPS',
    'indicative-aorist-neg-plural-third': '~IANPT',
    'indicative-aorist-neg-caus-singular-first': '~IANCSF',
    'indicative-aorist-neg-caus-singular-second': '~IANCSS',
    'indicative-aorist-neg-caus-singular-third': '~IANCST',
    'indicative-aorist-neg-caus-plural-first': '~IANCPF',
    'indicative-aorist-neg-caus-plural-second': '~IANCPS',
    'indicative-aorist-neg-caus-plural-third': '~IANCPT',
    'indicative-aorist-neg-passive-singular-first': '~IANPSF',
    'indicative-aorist-neg-passive-singular-second': '~IANPSS',
    'indicative-aorist-neg-passive-singular-third': '~IANPST',
    'indicative-aorist-neg-passive-plural-first': '~IANPPF',
    'indicative-aorist-neg-passive-plural-second': '~IANPPS',
    'indicative-aorist-neg-passive-plural-third': '~IANPPT',
    'indicative-aorist-neg-caus-passive-singular-first': '~IANCPSF',
    'indicative-aorist-neg-caus-passive-singular-second': '~IANCPSS',
    'indicative-aorist-neg-caus-passive-singular-third': '~IANCPST',
    'indicative-aorist-neg-caus-passive-plural-first': '~IANCPPF',
    'indicative-aorist-neg-caus-passive-plural-second': '~IANCPPS',
    'indicative-aorist-neg-caus-passive-plural-third': '~IANCPPT',
    'subjunctive-future-singular-first': '~SFSF',
    'subjunctive-future-singular-second': '~SFSS',
    'subjunctive-future-singular-third': '~SFST',
    'subjunctive-future-plural-first': '~SFPF',
    'subjunctive-future-plural-second': '~SFPS',
    'subjunctive-future-plural-third': '~SFPT',
    'subjunctive-future-caus-singular-first': '~SFCSF',
    'subjunctive-future-caus-singular-second': '~SFCSS',
    'subjunctive-future-caus-singular-third': '~SFCST',
    'subjunctive-future-caus-plural-first': '~SFCPF',
    'subjunctive-future-caus-plural-second': '~SFCPS',
    'subjunctive-future-caus-plural-third': '~SFCPT',
    'subjunctive-future-passive-singular-first': '~SFPSF',
    'subjunctive-future-passive-singular-second': '~SFPSS',
    'subjunctive-future-passive-singular-third': '~SFPST',
    'subjunctive-future-passive-plural-first': '~SFPPF',
    'subjunctive-future-passive-plural-second': '~SFPPS',
    'subjunctive-future-passive-plural-third': '~SFPPT',
    'subjunctive-future-caus-passive-singular-first': '~SFCPSF',
    'subjunctive-future-caus-passive-singular-second': '~SFCPSS',
    'subjunctive-future-caus-passive-singular-third': '~SFCPST',
    'subjunctive-future-caus-passive-plural-first': '~SFCPPF',
    'subjunctive-future-caus-passive-plural-second': '~SFCPPS',
    'subjunctive-future-caus-passive-plural-third': '~SFCPPT',
    'subjunctive-future-neg-singular-first': '~SFNSF',
    'subjunctive-future-neg-singular-second': '~SFNSS',
    'subjunctive-future-neg-singular-third': '~SFNST',
    'subjunctive-future-neg-plural-first': '~SFNPF',
    'subjunctive-future-neg-plural-second': '~SFNPS',
    'subjunctive-future-neg-plural-third': '~SFNPT',
    'subjunctive-future-neg-caus-singular-first': '~SFNCSF',
    'subjunctive-future-neg-caus-singular-second': '~SFNCSS',
    'subjunctive-future-neg-caus-singular-third': '~SFNCST',
    'subjunctive-future-neg-caus-plural-first': '~SFNCPF',
    'subjunctive-future-neg-caus-plural-second': '~SFNCPS',
    'subjunctive-future-neg-caus-plural-third': '~SFNCPT',
    'subjunctive-future-neg-passive-singular-first': '~SFNPSF',
    'subjunctive-future-neg-passive-singular-second': '~SFNPSS',
    'subjunctive-future-neg-passive-singular-third': '~SFNPST',
    'subjunctive-future-neg-passive-plural-first': '~SFNPPF',
    'subjunctive-future-neg-passive-plural-second': '~SFNPPS',
    'subjunctive-future-neg-passive-plural-third': '~SFNPPT',
    'subjunctive-future-neg-caus-passive-singular-first': '~SFNCPSF',
    'subjunctive-future-neg-caus-passive-singular-second': '~SFNCPSS',
    'subjunctive-future-neg-caus-passive-singular-third': '~SFNCPST',
    'subjunctive-future-neg-caus-passive-plural-first': '~SFNCPPF',
    'subjunctive-future-neg-caus-passive-plural-second': '~SFNCPPS',
    'subjunctive-future-neg-caus-passive-plural-third': '~SFNCPPT',
    'subjunctive-future_perfect-singular-first': '~SFPSF',
    'subjunctive-future_perfect-singular-second': '~SFPSS',
    'subjunctive-future_perfect-singular-third': '~SFPST',
    'subjunctive-future_perfect-plural-first': '~SFPPF',
    'subjunctive-future_perfect-plural-second': '~SFPPS',
    'subjunctive-future_perfect-plural-third': '~SFPPT',
    'subjunctive-future_perfect-caus-singular-first': '~SFPCSF',
    'subjunctive-future_perfect-caus-singular-second': '~SFPCSS',
    'subjunctive-future_perfect-caus-singular-third': '~SFPCST',
    'subjunctive-future_perfect-caus-plural-first': '~SFPCPF',
    'subjunctive-future_perfect-caus-plural-second': '~SFPCPS',
    'subjunctive-future_perfect-caus-plural-third': '~SFPCPT',
    'subjunctive-future_perfect-passive-singular-first': '~SFPPSF',
    'subjunctive-future_perfect-passive-singular-second': '~SFPPSS',
    'subjunctive-future_perfect-passive-singular-third': '~SFPPST',
    'subjunctive-future_perfect-passive-plural-first': '~SFPPPF',
    'subjunctive-future_perfect-passive-plural-second': '~SFPPPS',
    'subjunctive-future_perfect-passive-plural-third': '~SFPPPT',
    'subjunctive-future_perfect-caus-passive-singular-first': '~SFPCPSF',
    'subjunctive-future_perfect-caus-passive-singular-second': '~SFPCPSS',
    'subjunctive-future_perfect-caus-passive-singular-third': '~SFPCPST',
    'subjunctive-future_perfect-caus-passive-plural-first': '~SFPCPPF',
    'subjunctive-future_perfect-caus-passive-plural-second': '~SFPCPPS',
    'subjunctive-future_perfect-caus-passive-plural-third': '~SFPCPPT',
    'subjunctive-future_perfect-neg-singular-first': '~SFPNSF',
    'subjunctive-future_perfect-neg-singular-second': '~SFPNSS',
    'subjunctive-future_perfect-neg-singular-third': '~SFPNST',
    'subjunctive-future_perfect-neg-plural-first': '~SFPNPF',
    'subjunctive-future_perfect-neg-plural-second': '~SFPNPS',
    'subjunctive-future_perfect-neg-plural-third': '~SFPNPT',
    'subjunctive-future_perfect-neg-caus-singular-first': '~SFPNCSF',
    'subjunctive-future_perfect-neg-caus-singular-second': '~SFPNCSS',
    'subjunctive-future_perfect-neg-caus-singular-third': '~SFPNCST',
    'subjunctive-future_perfect-neg-caus-plural-first': '~SFPNCPF',
    'subjunctive-future_perfect-neg-caus-plural-second': '~SFPNCPS',
    'subjunctive-future_perfect-neg-caus-plural-third': '~SFPNCPT',
    'subjunctive-future_perfect-neg-passive-singular-first': '~SFPNPSF',
    'subjunctive-future_perfect-neg-passive-singular-second': '~SFPNPSS',
    'subjunctive-future_perfect-neg-passive-singular-third': '~SFPNPST',
    'subjunctive-future_perfect-neg-passive-plural-first': '~SFPNPPF',
    'subjunctive-future_perfect-neg-passive-plural-second': '~SFPNPPS',
    'subjunctive-future_perfect-neg-passive-plural-third': '~SFPNPPT',
    'subjunctive-future_perfect-neg-caus-passive-singular-first': '~SFPNCPSF',
    'subjunctive-future_perfect-neg-caus-passive-singular-second': '~SFPNCPSS',
    'subjunctive-future_perfect-neg-caus-passive-singular-third': '~SFPNCPST',
    'subjunctive-future_perfect-neg-caus-passive-plural-first': '~SFPNCPPF',
    'subjunctive-future_perfect-neg-caus-passive-plural-second': '~SFPNCPPS',
    'subjunctive-future_perfect-neg-caus-passive-plural-third': '~SFPNCPPT',
    'conditional-future-singular-first': '~CFSF',
    'conditional-future-singular-second': '~CFSS',
    'conditional-future-singular-third': '~CFST',
    'conditional-future-plural-first': '~CFPF',
    'conditional-future-plural-second': '~CFPS',
    'conditional-future-plural-third': '~CFPT',
    'conditional-future-caus-singular-first': '~CFCSF',
    'conditional-future-caus-singular-second': '~CFCSS',
    'conditional-future-caus-singular-third': '~CFCST',
    'conditional-future-caus-plural-first': '~CFCPF',
    'conditional-future-caus-plural-second': '~CFCPS',
    'conditional-future-caus-plural-third': '~CFCPT',
    'conditional-future-passive-singular-first': '~CFPSF',
    'conditional-future-passive-singular-second': '~CFPSS',
    'conditional-future-passive-singular-third': '~CFPST',
    'conditional-future-passive-plural-first': '~CFPPF',
    'conditional-future-passive-plural-second': '~CFPPS',
    'conditional-future-passive-plural-third': '~CFPPT',
    'conditional-future-caus-passive-singular-first': '~CFCPSF',
    'conditional-future-caus-passive-singular-second': '~CFCPSS',
    'conditional-future-caus-passive-singular-third': '~CFCPST',
    'conditional-future-caus-passive-plural-first': '~CFCPPF',
    'conditional-future-caus-passive-plural-second': '~CFCPPS',
    'conditional-future-caus-passive-plural-third': '~CFCPPT',
    'conditional-future_perfect-singular-first': '~CFPSF',
    'conditional-future_perfect-singular-second': '~CFPSS',
    'conditional-future_perfect-singular-third': '~CFPST',
    'conditional-future_perfect-plural-first': '~CFPPF',
    'conditional-future_perfect-plural-second': '~CFPPS',
    'conditional-future_perfect-plural-third': '~CFPPT',
    'conditional-future_perfect-caus-singular-first': '~CFPCSF',
    'conditional-future_perfect-caus-singular-second': '~CFPCSS',
    'conditional-future_perfect-caus-singular-third': '~CFPCST',
    'conditional-future_perfect-caus-plural-first': '~CFPCPF',
    'conditional-future_perfect-caus-plural-second': '~CFPCPS',
    'conditional-future_perfect-caus-plural-third': '~CFPCPT',
    'conditional-future_perfect-passive-singular-first': '~CFPPSF',
    'conditional-future_perfect-passive-singular-second': '~CFPPSS',
    'conditional-future_perfect-passive-singular-third': '~CFPPST',
    'conditional-future_perfect-passive-plural-first': '~CFPPPF',
    'conditional-future_perfect-passive-plural-second': '~CFPPPS',
    'conditional-future_perfect-passive-plural-third': '~CFPPPT',
    'conditional-future_perfect-caus-passive-singular-first': '~CFPCPSF',
    'conditional-future_perfect-caus-passive-singular-second': '~CFPCPSS',
    'conditional-future_perfect-caus-passive-singular-third': '~CFPCPST',
    'conditional-future_perfect-caus-passive-plural-first': '~CFPCPPF',
    'conditional-future_perfect-caus-passive-plural-second': '~CFPCPPS',
    'conditional-future_perfect-caus-passive-plural-third': '~CFPCPPT',
    'imperative-none-singular-second': '~INSS',
    'imperative-none-plural-second': '~INPS',
    'imperative-none-caus-singular-second': '~INCSS',
    'imperative-none-caus-plural-second': '~INCPS',
    'imperative-none-passive-singular-second': '~INPSS',
    'imperative-none-passive-plural-second': '~INPPS',
    'imperative-none-caus-passive-singular-second': '~INCPSS',
    'imperative-none-caus-passive-plural-second': '~INCPPS',
  }
  
  @staticmethod
  def elal( word ): 
    return word[:-2]
    
  @staticmethod
  def neg_ch( word ):
    return 'չ{}'.format(word)
  
  def parse_word( self, type ):
    func_name =  self.conjugations.get(type)
    
    try:
      if func_name[:1] == '-':
        func = getattr(self, '{}0'.format(func_name[1:]))
      else:
        func = getattr(self, '{}1'.format(func_name[1:]))
    except:
      if 'neg' in type.split('-'):
        norm_func = '-'.join(filter(lambda x: True if x != 'neg' else False, type.split('-')))
        n_func_name =  self.conjugations.get(norm_func)
        try:
          if n_func_name[:1] == '-':
            norm_func = getattr(self, '{}0'.format(n_func_name[1:]))
          else:
            norm_func = getattr(self, '{}1'.format(n_func_name[1:]))
        except:
          return False
        else:
          word = self.neg_ch(norm_func())
          return {
            'word': word,
          }
      else:
        return False
    else:
      word = func()
      return {
        'word': word,
      }
  
  def parse( self, type=False ):
    if type:
      if not self.conjugations.get(type):
        raise KeyError
      else:
        parsed = self.parse_word(type)
        if parsed:
          return parsed
    else:
      c_arr = []
      for c in self.conjugations:
        parsed = self.parse_word(c)
        if parsed:
          c_arr.append(parsed)
      return c_arr
      
  def save( self ):
    pass
    
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
    pass
    
  def word_attr( self, attr ):
    for u, v in self.attr:
      if u == attr:
        return v
    return ''
    
  def word_attr_k( self, attr ):
    for u, v in self.attr:
      if attr == v:
        return True
    return False
    
  def word_attr_val( self, attr ):
    for u, v in self.attr:
      if attr in v:
        return v.split('=')[-1]
    return False
  
  def __init__( self, word, attr, **kwargs ):
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
  
  def indicative_aorist_st( self, ending, caus=False, passive=False ):
    if caus and passive:
      tpl = '{}վեց{end}'
    else:
      tpl = '{}{caus}{passive}{end}'
    if self.word_attr_val('aor='):
      return tpl.format(self.word_attr_val('aor='), caus=('րեց' if caus else ''), passive=('վ' if passive else ''), end=ending[0])
    else:
      if self.word_attr(3):
        return tpl.format(self.word_attr(3), caus=('րեց' if caus else ''), passive=('վ' if passive else ''), end=ending[1])
      else:
        return tpl.format(self.elal(self.word), caus=('րեց' if caus else ''), passive=('վ' if passive else ''), end=ending[2])
  
  def imperative_none_st( self, ending, caus=False, passive=False ):
    if caus and passive:
      tpl = '{}վեց{end}'
    else:
      tpl = '{}{caus}{passive}{end}'
    if self.word_attr(3):
      return tpl.format(self.word_attr(3), caus=('եցր' if caus else ''), passive=('վ' if passive else ''), end=ending)
    else:
      return tpl.format(self.elal(self.word), caus=('եցր' if caus else ''), passive=('վ' if passive else ''), end=ending)
  
  def standart_st( self, ending, caus=False, passive=False, conditional=False ):
    if caus and passive:
      tpl = '{}եցվ{end}'
    else:
      tpl = '{}{caus}{passive}{end}'
    if conditional:
      tpl = ''.join(['կ', tpl])
    return tpl.format(self.elal(self.word), caus=('եցն' if caus else ''), passive=('վ' if passive else ''), end=ending)
  
class VerbElParser(VerbParser):
  def IASF1( self ):
    return self.indicative_aorist_st(['ի', 'ա', 'եցի'])
    
  def IASS1( self ):
    return self.indicative_aorist_st(['իր', 'ար', 'եցիր'])
    
  def IAST1( self ):
    return self.indicative_aorist_st(['', 'ավ', 'եց'])
      
  def IAPF1( self ):
    return self.indicative_aorist_st(['ինք', 'անք', 'եցինք'])
    
  def IAPS1( self ):
    return self.indicative_aorist_st(['իք', 'աք', 'եցիք'])
    
  def IAPT1( self ):
    return self.indicative_aorist_st(['ին', 'ան', 'եցին'])
    
  def IACSF1( self ):
    return self.indicative_aorist_st(['ի', 'ա', 'եցի'], caus=True)
    
  def IACSS1( self ):
    return self.indicative_aorist_st(['իր', 'ար', 'եցիր'], caus=True)
    
  def IACST1( self ):
    return self.indicative_aorist_st(['', 'ավ', 'եց'], caus=True)
      
  def IACPF1( self ):
    return self.indicative_aorist_st(['ինք', 'անք', 'եցինք'], caus=True)
    
  def IACPS1( self ):
    return self.indicative_aorist_st(['իք', 'աք', 'եցիք'], caus=True)
    
  def IACPT1( self ):
    return self.indicative_aorist_st(['ին', 'ան', 'եցին'], caus=True)
  
  def IAPSF1( self ):
    return self.indicative_aorist_st(['ի', 'ա', 'եցի'], passive=True)
    
  def IAPSS1( self ):
    return self.indicative_aorist_st(['իր', 'ար', 'եցիր'], passive=True)
    
  def IAPST1( self ):
    return self.indicative_aorist_st(['եց', 'ավ', 'եց'], passive=True)
      
  def IAPPF1( self ):
    return self.indicative_aorist_st(['ինք', 'անք', 'եցինք'], passive=True)
    
  def IAPPS1( self ):
    return self.indicative_aorist_st(['իք', 'աք', 'եցիք'], passive=True)
    
  def IAPPT1( self ):
    return self.indicative_aorist_st(['ին', 'ան', 'եցին'], passive=True)
    
  def IACPSF1( self ):
    return self.indicative_aorist_st(['ի', 'ա', 'եցի'], caus=True, passive=True)
    
  def IACPSS1( self ):
    return self.indicative_aorist_st(['իր', 'ար', 'եցիր'], caus=True, passive=True)
    
  def IACPST1( self ):
    return self.indicative_aorist_st(['', 'ավ', 'եց'], caus=True, passive=True)
      
  def IACPPF1( self ):
    return self.indicative_aorist_st(['ինք', 'անք', 'եցինք'], caus=True, passive=True)
    
  def IACPPS1( self ):
    return self.indicative_aorist_st(['իք', 'աք', 'եցիք'], caus=True, passive=True)
    
  def IACPPT1( self ):
    return self.indicative_aorist_st(['ին', 'ան', 'եցին'], caus=True, passive=True) 
    
  def SFSF1( self ):
    return self.standart_st('եմ')
    
  def SFSS1( self ):
    return self.standart_st('ես')
    
  def SFST1( self ):
    return self.standart_st('ի')
    
  def SFPF1( self ):
    return self.standart_st('ենք')
    
  def SFPS1( self ):
    return self.standart_st('եք')
    
  def SFPT1( self ):
    return self.standart_st('են')
    
  def SFCSF1( self ):
    return self.standart_st('եմ', caus=True)
    
  def SFCSS1( self ):
    return self.standart_st('ես', caus=True)
    
  def SFCST1( self ):
    return self.standart_st('ի', caus=True)
    
  def SFCPF1( self ):
    return self.standart_st('ենք', caus=True)
    
  def SFCPS1( self ):
    return self.standart_st('եք', caus=True)
    
  def SFCPT1( self ):
    return self.standart_st('են', caus=True)
    
  def SFPSF1( self ):
    return self.standart_st('եմ', passive=True)
    
  def SFPSS1( self ):
    return self.standart_st('ես', passive=True)
    
  def SFPST1( self ):
    return self.standart_st('ի', passive=True)
    
  def SFPPF1( self ):
    return self.standart_st('ենք', passive=True)
    
  def SFPPS1( self ):
    return self.standart_st('եք', passive=True)
    
  def SFPPT1( self ):
    return self.standart_st('են', passive=True)
    
  def SFCPSF1( self ):
    return self.standart_st('եմ', caus=True, passive=True)
    
  def SFCPSS1( self ):
    return self.standart_st('ես', caus=True, passive=True)
    
  def SFCPST1( self ):
    return self.standart_st('ի', caus=True, passive=True)
    
  def SFCPPF1( self ):
    return self.standart_st('ենք', caus=True, passive=True)
    
  def SFCPPS1( self ):
    return self.standart_st('եք', caus=True, passive=True)
    
  def SFCPPT1( self ):
    return self.standart_st('են', caus=True, passive=True)
  
  def SFPSF1( self ):
    return self.standart_st('եի')
    
  def SFPSS1( self ):
    return self.standart_st('եիր')
    
  def SFPST1( self ):
    return self.standart_st('եք')
    
  def SFPPF1( self ):
    return self.standart_st('եինք')
    
  def SFPPS1( self ):
    return self.standart_st('եիք')
    
  def SFPPT1( self ):
    return self.standart_st('եին')
    
  def SFPCSF1( self ):
    return self.standart_st('եի', caus=True)
    
  def SFPCSS1( self ):
    return self.standart_st('եիր', caus=True)
    
  def SFPCST1( self ):
    return self.standart_st('եիք', caus=True)
    
  def SFPCPF1( self ):
    return self.standart_st('եինք', caus=True)
    
  def SFPCPS1( self ):
    return self.standart_st('եիք', caus=True)
    
  def SFPCPT1( self ):
    return self.standart_st('եին', caus=True)
    
  def SFPPSF1( self ):
    return self.standart_st('եի', passive=True)
    
  def SFPPSS1( self ):
    return self.standart_st('եիր', passive=True)
    
  def SFPPST1( self ):
    return self.standart_st('եիք', passive=True)
    
  def SFPPPF1( self ):
    return self.standart_st('եինք', passive=True)
    
  def SFPPPS1( self ):
    return self.standart_st('եիք', passive=True)
    
  def SFPPPT1( self ):
    return self.standart_st('եին', passive=True)
    
  def SFPCPSF1( self ):
    return self.standart_st('եի', caus=True, passive=True)
    
  def SFPCPSS1( self ):
    return self.standart_st('եիր', caus=True, passive=True)
    
  def SFPCPST1( self ):
    return self.standart_st('եիք', caus=True, passive=True)
    
  def SFPCPPF1( self ):
    return self.standart_st('եինք', caus=True, passive=True)
    
  def SFPCPPS1( self ):
    return self.standart_st('եիք', caus=True, passive=True)
    
  def SFPCPPT1( self ):
    return self.standart_st('եին', caus=True, passive=True)
  
  def CFSF1( self ):
    return self.standart_st('եմ')
    
  def CFSS1( self ):
    return self.standart_st('ես', conditional=True)
    
  def CFST1( self ):
    return self.standart_st('ի', conditional=True)
    
  def CFPF1( self ):
    return self.standart_st('ենք', conditional=True)
    
  def CFPS1( self ):
    return self.standart_st('եք', conditional=True)
    
  def CFPT1( self ):
    return self.standart_st('են', conditional=True)
    
  def CFCSF1( self ):
    return self.standart_st('եմ', caus=True, conditional=True)
    
  def CFCSS1( self ):
    return self.standart_st('ես', caus=True, conditional=True)
    
  def CFCST1( self ):
    return self.standart_st('ի', caus=True, conditional=True)
    
  def CFCPF1( self ):
    return self.standart_st('ենք', caus=True, conditional=True)
    
  def CFCPS1( self ):
    return self.standart_st('եք', caus=True, conditional=True)
    
  def CFCPT1( self ):
    return self.standart_st('են', caus=True, conditional=True)
    
  def CFPSF1( self ):
    return self.standart_st('եմ', passive=True, conditional=True)
    
  def CFPSS1( self ):
    return self.standart_st('ես', passive=True, conditional=True)
    
  def CFPST1( self ):
    return self.standart_st('ի', passive=True, conditional=True)
    
  def CFPPF1( self ):
    return self.standart_st('ենք', passive=True, conditional=True)
    
  def CFPPS1( self ):
    return self.standart_st('եք', passive=True, conditional=True)
    
  def CFPPT1( self ):
    return self.standart_st('են', passive=True, conditional=True)
    
  def CFCPSF1( self ):
    return self.standart_st('եմ', caus=True, passive=True, conditional=True)
    
  def CFCPSS1( self ):
    return self.standart_st('ես', caus=True, passive=True, conditional=True)
    
  def CFCPST1( self ):
    return self.standart_st('ի', caus=True, passive=True, conditional=True)
    
  def CFCPPF1( self ):
    return self.standart_st('ենք', caus=True, passive=True, conditional=True)
    
  def CFCPPS1( self ):
    return self.standart_st('եք', caus=True, passive=True, conditional=True)
    
  def CFCPPT1( self ):
    return self.standart_st('են', caus=True, passive=True, conditional=True)
  
  def CFPSF1( self ):
    return self.standart_st('եի', conditional=True)
    
  def CFPSS1( self ):
    return self.standart_st('եիր', conditional=True)
    
  def CFPST1( self ):
    return self.standart_st('եք', conditional=True)
    
  def CFPPF1( self ):
    return self.standart_st('եինք', conditional=True)
    
  def CFPPS1( self ):
    return self.standart_st('եիք', conditional=True)
    
  def CFPPT1( self ):
    return self.standart_st('եին', conditional=True)
    
  def CFPCSF1( self ):
    return self.standart_st('եի', caus=True, conditional=True)
    
  def CFPCSS1( self ):
    return self.standart_st('եիր', caus=True, conditional=True)
    
  def CFPCST1( self ):
    return self.standart_st('եիք', caus=True, conditional=True)
    
  def CFPCPF1( self ):
    return self.standart_st('եինք', caus=True, conditional=True)
    
  def CFPCPS1( self ):
    return self.standart_st('եիք', caus=True, conditional=True)
    
  def CFPCPT1( self ):
    return self.standart_st('եին', caus=True, conditional=True)
    
  def CFPPSF1( self ):
    return self.standart_st('եի', passive=True, conditional=True)
    
  def CFPPSS1( self ):
    return self.standart_st('եիր', passive=True, conditional=True)
    
  def CFPPST1( self ):
    return self.standart_st('եիք', passive=True, conditional=True)
    
  def CFPPPF1( self ):
    return self.standart_st('եինք', passive=True, conditional=True)
    
  def CFPPPS1( self ):
    return self.standart_st('եիք', passive=True, conditional=True)
    
  def CFPPPT1( self ):
    return self.standart_st('եին', passive=True, conditional=True)
    
  def CFPCPSF1( self ):
    return self.standart_st('եի', caus=True, passive=True, conditional=True)
    
  def CFPCPSS1( self ):
    return self.standart_st('եիր', caus=True, passive=True, conditional=True)
    
  def CFPCPST1( self ):
    return self.standart_st('եիք', caus=True, passive=True, conditional=True)
    
  def CFPCPPF1( self ):
    return self.standart_st('եինք', caus=True, passive=True, conditional=True)
    
  def CFPCPPS1( self ):
    return self.standart_st('եիք', caus=True, passive=True, conditional=True)
    
  def CFPCPPT1( self ):
    return self.standart_st('եին', caus=True, passive=True, conditional=True)

  def INSS1( self ):
    return self.imperative_none_st('իր')
    
  def INPS1( self ):
    return self.imperative_none_st('եք')
    
  def INCSS1( self ):
    return self.imperative_none_st('ու', caus=True)
    
  def INCPS1( self ):
    return self.imperative_none_st('եք', caus=True)
  
  def INPSS1( self ):
    return self.imperative_none_st('իր', passive=True)
    
  def INPPS1( self ):
    return self.imperative_none_st('եք', passive=True)
    
  def INCPSS1( self ):
    return self.imperative_none_st('րու', caus=True, passive=True)
    
  def INCPPS1( self ):
    return self.imperative_none_st('եք', caus=True, passive=True)
    
class VerbParserFactory:
  parsers = {
    'ել' : VerbElParser,
  }
  
  @classmethod
  def parser( cls, word, attr, **kwargs ):
    type = re.split(r'\|(?=\|*)', attr[2:-2])[0][8:]
    if not type or not cls.parsers.get( type ):
      raise KeyError
    else:
      return cls.parsers.get( type )( word, attr )

if __name__ == '__main__':

  #թողնել, {{hy-conj-ել|թողն||թող|aor=թողեց|}}
  #parser = VerbParserFactory.parser('թողնել', '{{hy-conj-ել|թողն||թող|aor=թողեց}}')
  parser = VerbParserFactory.parser('վազել', '{{hy-conj-ել|aor=վազեց}}')
  #parser = VerbParserFactory.parser('գրել', '{{hy-conj-ել|aor=գրեց}}')
  output = [parser.parse('imperative-none-caus-passive-singular-second')]
  output = parser.parse()

  file = open('vazel.txt', 'w', encoding='utf-8')
  for o in output:
    file.write(o['word'] + '\n')
  file.close()
