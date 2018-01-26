from django.db import models

from bibliography.models import Text
from .features import *

class Sentence(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  sentence = models.TextField()
  position = models.IntegerField()
  text = models.ForeignKey(Text)
  
  def __str__(self):
    return '{s}'.format(s=self.sentence)
  
class Token(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  token = models.CharField(max_length=250)
  position = models.CharField(max_length=5)
  sentence = models.ForeignKey(Sentence)
  arc = models.IntegerField(default=0, blank=True)
  arc_label = models.CharField(max_length=50, blank=True)
  trim_spaceafter = models.BooleanField(default=False)
  tag = models.ManyToManyField('tokenization.Word', blank=True)
  selected_tag = models.ForeignKey('tokenization.Word', related_name='selected_tag', blank=True, null=True)
  checked = models.BooleanField(default=False)
  
  def __str__(self):
    return '{t}'.format(t=self.token)
  
class Word(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)  
  POS_CHOICES = (
    ('noun', 'Noun'), #NOUN, PROPN
    ('verb', 'Verb'), #VERB
    ('punct', 'Punct'), #PUNCT
    ('sym', 'Sym'), #SYM
    ('x', 'X'), #X
    ('intj', 'Interjection'), #INTJ
    ('adj', 'Adjective'), #ADJ
    ('adv', 'Adverb'), #ADV
    ('det', 'Det'), #DET
    ('sconj', 'Sconj'), #SCONJ
    ('cconj', 'Cconj'), #CCONJ
    ('num', 'Numeral'), #NUM
    ('part', 'Part'), #PART
    ('pron', 'Pron'), #PRON
    ('aux', 'Aux'), #AUX
    ('adp', 'Adp'), #ADP
  )
  pos = models.CharField(
    max_length=25,
    choices=POS_CHOICES,
    blank=True,
  )
  word = models.CharField(max_length=250)
  
  def __str__(self):
    return '{t}'.format(t=self.word)

#ok parser-default+
class Sconj(models.Model):
  POS = 'sconj'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+
class Cconj(models.Model):
  POS = 'cconj'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  conj_type = conj_type

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-pass+
class Numeral(models.Model):
  POS = 'num'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  num_type = num_type
  num_form = num_form

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+
class Part(models.Model):
  POS = 'part'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  mood = mood

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-pass+
class Pron(models.Model):
  POS = 'pron'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  animacy = animacy
  case = case
  person = person
  reflex = reflex
  poss_number = poss_number
  poss_person = poss_person
  number = number

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+ 
class Aux(models.Model):
  POS = 'aux'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  aspect = aspect
  mood = mood
  person = person
  polarity = polarity
  subcat = subcat
  tense = tense
  verb_form = verb_form
  voice = voice
  number = number

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-pass+
class Adp(models.Model):
  POS = 'adp'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  adp_type = adp_type
  case = case
  poss_number = poss_number
  poss_person = poss_person

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok? parser-pass+
class Det(models.Model):
  POS = 'det'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  definite = definite
  person = person
  pron_type = pron_type
  reflex = reflex
  poss_number = poss_number
  poss_person = poss_person
  
  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-pass+
class Intj(models.Model):
  POS = 'intj'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  value_sym = models.CharField(max_length=250)
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  
  def __str__(self):
    return self.value_sym

#ok parser-default+
class Adv(models.Model):
  POS = 'adv'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  degree = degree
  hyph = hyph
  name_type = name_type
  num_type = num_type
  pron_type = pron_type

  def __str__(self):
    return '{t}'.format(t=self.parent)
    
#ok parser-default+
class Adj(models.Model):
  POS = 'adj'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  degree = degree
  hyph = hyph
  name_type = name_type
  num_type = num_type
  verb_form = verb_form
  voice = voice
  
  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+
class Punct(models.Model):
  POS = 'punct'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+
class Sym(models.Model):
  POS = 'sym'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-default+
class X(models.Model):
  POS = 'x'
  parent = models.OneToOneField('tokenization.Word', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok parser-pass+
class Noun(models.Model):
  POS = 'noun'
  parent = models.OneToOneField('tokenization.Word', related_name='n_parent', blank=True, null=True, editable=False)
  lemma = lemma
  animacy = models.ManyToManyField('tokenization.NounAnimacy', related_name='n_animacy', blank=True)
  proper = models.BooleanField(default=False)
  case = case
  definite = definite
  number = number
  poss_number = poss_number
  poss_person = poss_person
  verb_form = verb_form
  name_type = name_type
  materiality = materiality
  nominalized = nominalized
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign

  def __str__(self):
    return '{t}'.format(t=self.parent)

#ok +
class NounAnimacy(models.Model):
  title = models.CharField(max_length=20)
  value = models.CharField(max_length=20)
  
  def __str__(self):
    return self.value

#pass ++
class Verb(models.Model):
  POS = 'verb'
  parent = models.OneToOneField('tokenization.Word', related_name='v_parent', blank=True, null=True, editable=False)
  lemma = lemma
  abbr = abbr
  poss = poss
  echo = echo
  foreign = foreign
  verb_form = verb_form #1t.
  aspect = aspect #1t.
  mood = mood #1t.
  person = person #1t.
  polarity = polarity #1t.
  tense = tense #1t.
  number = number #2t.
  poss_number = poss_number #2t.
  poss_person = poss_person #2t.
  subcat = subcat #2t.
  voice_feat = models.CharField( #1t.
    max_length=5,
    choices=(('act', 'Act'),
             ('cau', 'Cau'),
             ('mid', 'Mid'),
             ('pass', 'Pass'),
            ),
    blank=True,
  )
  voice = models.CharField(choices=( #2t.
      ('middle', 'ՉԲ'),
      ('active', 'ՆԲ'),
    ), max_length=8, default='middle')
  
  def __str__(self):
    return '{t}'.format(t=self.parent)

  '''
  #VERBS
  ending = models.CharField(max_length=250, blank=True)
  root = models.CharField(max_length=250, blank=True)
  type = models.CharField(max_length=250, blank=True)
  form = models.CharField(max_length=250, blank=True)
  QUANTITY_CHOICES = (
    (1, 'Singular'),
    (2, 'Plural'),
  )
  quantity = models.CharField(
    max_length=10,
    choices=QUANTITY_CHOICES,
    blank=True,
  )
  DEMQ_CHOICES = (
    (1, 'First'),
    (2, 'Second'),
    (3, 'Third'),
  )
  demq = models.CharField(
    max_length=3,
    choices=DEMQ_CHOICES,
    blank=True,
  )
  
  declension_type = models.CharField(max_length=25, blank=True)
  DECLENSION_CHOICES = (
    ('nominative', 'Nominative'),
    ('dative', 'Dative'),
    ('ablative', 'Ablative'),
    ('instrumental', 'Instrumental'),
    ('locative', 'Locative'),
  )
  declension = models.CharField(
    max_length=20,
    choices=DECLENSION_CHOICES,
    blank=True,
  )
  QUANTITY_TYPE_CHOICES = (
    ('', '-'),
    ('եր', '-եր'),
    ('ներ', '-ներ'),
  )
  quantity_type = models.CharField(
    max_length=10,
    choices=QUANTITY_TYPE_CHOICES,
    blank=True,
  )
  DEFINITE_CHOICES = (
    ('empty', 'Empty'),
    ('def', 'Definite'),
    ('indef', 'Indefinite'),
  )
  definite = models.CharField(
    max_length=8,
    choices=DEFINITE_CHOICES,
    blank=True,
  )
  QUANTITY_CHOICES = (
    ('singular', 'Singular'),
    ('plural', 'Plural'),
    ('collective', 'Collective'),
    ('assocpl', 'Associative'),
  )
  quantity = models.CharField(
    max_length=15,
    choices=QUANTITY_CHOICES,
    blank=True,
  )
  oblique_stem = models.CharField(max_length=256, blank=True)
  singular_stem = models.CharField(max_length=256, blank=True)
  proper = models.BooleanField(default=False)
  MATERIALITY_CHOICES = (
    ('conc', 'concrete'),
    ('astr', 'abstract'),
  )
  materiality = models.CharField(
    max_length=10,
    choices=MATERIALITY_CHOICES,
    blank=True,
  )
  POSSNUMBER_CHOICES = (
    ('singular', 'Singular'),
    ('plural', 'Plural'),
  )
  poss_number = models.CharField(
    max_length=10,
    choices=POSSNUMBER_CHOICES,
    blank=True,
  )
  POSSPERSON_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
  )
  poss_person = models.CharField(
    max_length=10,
    choices=POSSPERSON_CHOICES,
    blank=True,
  )
  animacy = models.ManyToManyField('tokenization.NounAnimacy', blank=True)
  '''
