from django.db import models

from bibliography.models import Text

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
  tag = models.ManyToManyField('tokenization.Word', blank=True, null=True)
  selected_tag = models.ForeignKey('tokenization.Word', related_name='selected_tag', blank=True, null=True)
  checked = models.BooleanField(default=False)
  
  def __str__(self):
    return '{t}'.format(t=self.token)

class Word(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)  
  POS_CHOICES = (
    ('noun', 'Noun'),
    ('verb', 'Verb'),
  )
  pos = models.CharField(
    max_length=25,
    choices=POS_CHOICES,
    blank=True,
  )
  word = models.CharField(max_length=250)
  lemma = models.ForeignKey('tokenization.Word', related_name='w_lemma', null=True, blank=True)
  
  def __str__(self):
    return '{t}'.format(t=self.word)
    
class Noun(models.Model):
  parent = models.OneToOneField('tokenization.Word', related_name='n_parent')
  oblique_stem = models.CharField(max_length=256, blank=True)
  singular_stem = models.CharField(max_length=256, blank=True)
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
  QUANTITY_CHOICES = (
    ('singular', 'Singular'),
    ('plural', 'Plural'),
  )
  quantity = models.CharField(
    max_length=10,
    choices=QUANTITY_CHOICES,
    blank=True,
  )
  QUANTITY_TYPE_CHOICES = (
    ('եր', '-եր'),
    ('ներ', '-ներ'),
  )
  quantity_type = models.CharField(
    max_length=10,
    choices=QUANTITY_TYPE_CHOICES,
    blank=True,
  )
  FORM_CHOICES = (
    ('', 'None'),
    ('definite', 'Definite'),
    ('first', 'First'),
    ('second', 'Second'),
  )
  form = models.CharField(
    max_length=10,
    choices=FORM_CHOICES,
    blank=True,
  )
  animate = models.BooleanField(default=False)
  uncountable = models.BooleanField(default=False)
  plural_only = models.BooleanField(default=False)
  nominalized = models.BooleanField(default=False)
  
  def __str__(self):
    return '{t}'.format(t=self.parent)
    
class Verb(models.Model):
  parent = models.OneToOneField('tokenization.Word', related_name='v_parent')
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
  
  def __str__(self):
    return '{t}'.format(t=self.parent)