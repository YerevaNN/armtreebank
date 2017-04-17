import re

from django.db import models
from user.models import UserProfile

class Author(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=250)
  patronymic = models.CharField(max_length=250,blank=True,null=True)
  pseudonym = models.CharField(max_length=250,blank=True,null=True)
  birth_date = models.CharField(max_length=15)
  death_date = models.CharField(max_length=15)
  
  def __str__(self):
    return '{} {} \ {}'.format(self.name, self.birth_date, self.death_date if self.death_date != '0' else '-' )
  
  @staticmethod
  def valid_date(str):
    if re.match(r'^[0-9]{1,4}([-|/][0-9]{2,4})*([-|/][0-9]{2,4})*$', str):
      return str
    return ''
  
  @staticmethod
  def create_author(request, form):
    response = {
      'type': 'error',
      'response': 'Սխալմունք'
    }
  
    author = Author()
    author.name = " ".join(" ".join(form.get('author_name').split(',')).split())
    author.patronymic = form.get('author_patronymic')
    author.pseudonym = form.get('author_pseudonym')
    author.birth_date = form.get('author_birth_date')
    author.death_date = form.get('author_death_date')
    
    try:
      author.clean_fields()
      author.save()
    except Exception:
      response['response'] = 'Թերի են լրացված հեղինակի տվյալները'
      return response
    
    response = {
      'type': 'ok',
      'response': '',
      'author': author,
    }
    return response

class Text(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  author = models.ManyToManyField(Author,blank=True)
  text_name = models.CharField(max_length=400,blank=True,null=True)
  text = models.TextField()
  LANG_CHOICES = (
    ('eastern', 'Արևելահայերեն'),
    ('western', 'Արևմտահայերեն'),
    ('middle', 'Միջին հայերեն'),
    ('grabar', 'Գրաբար'),
  )
  language = models.CharField(
    max_length=20,
    choices=LANG_CHOICES,
    default='eastern',
  )
  DIALECT_CHOICES = (
    ('literary', 'Գրական'),
    ('dialect', 'Բարբառային'),
  )
  dialect = models.CharField(
    max_length=20,
    choices=DIALECT_CHOICES,
    default='literary',
  )
  SPELLING_CHOICES = (
    ('modern_current', 'Արդի (1940-ներկա)'),
    ('modern_old', 'Արդի (1922-1940)'),
    ('classic', 'Դասական'),
  )
  spelling = models.CharField(
    max_length=20,
    choices=SPELLING_CHOICES,
    default='modern_current',
  )
  LETTER_CHOICES = (
    ('1', 'եւ'),
    ('2', 'և'),
  )
  ev_letter = models.CharField(
    max_length=2,
    choices=LETTER_CHOICES,
    default='1',
  )
  
  def __str__(self):
    return '{:.20}'.format(self.text)
  
  @staticmethod
  def save_text(form, author_required=True, count=1):
    response = {
      'type': 'error',
      'response': 'Սխալմունք'
    }
    texts = []
    
    for i in range(count):
      text = Text()
      text.text = form.get('text{pk}'.format(pk=i))
      text.text_name = form.get('text_name{pk}'.format(pk=i))
      text.language = form.get('language{pk}'.format(pk=i))
      text.dialect = form.get('dialect{pk}'.format(pk=i))
      text.spelling = form.get('spelling{pk}'.format(pk=i))
      text.ev_letter = form.get('ev_letter{pk}'.format(pk=i))
      try:
        text.clean_fields()
      except Exception:
        response['response'] = 'Լրացրեք տեքստը'
        return response
      
      if len(form.getlist('author{pk}[]'.format(pk=i))) == 0 and author_required:
        response['response'] = 'Նշեք հեղինակին'
        return response
        
      if len(form.getlist('author{pk}[]'.format(pk=i))):
        try:
          text.save()
        except Exception:
          return response
        
        for a in form.getlist('author{pk}[]'.format(pk=i)):
          if a:
            text.author.add(Author.objects.get(pk=a))
      
      try:
        text.save()
        texts.append(text)
      except Exception:
        return response
    
    response = {
      'type': 'ok',
      'response': 'Ավելացված է',
      'text': texts[0] if count == 1 else texts
    }
    return response

class Bibliography(models.Model):
  creation_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)
  profile = models.ForeignKey(UserProfile)
  name = models.CharField(max_length=650)
  tokens_count = models.IntegerField(default=0)
  LICENSE_CHOICES = (
    ('private', 'Պաշտպանված է հեղինակային իրավունքով'),
    ('public', 'Հանրային սեփականություն'),
  )
  license = models.CharField(
    max_length=20,
    choices=LICENSE_CHOICES,
    default='public',
  )
  TOKEN_CHOICES = (
    ('no', 'Թոքենիզացված չէ'),
    ('yes', 'Թոքենիզացված է'),
    ('validated', 'Թոքենիզացված է, ստուգված է'),
  )
  tokenized = models.CharField(
    max_length=20,
    choices=TOKEN_CHOICES,
    default='no',
  )
  
  def __str__(self):
    return '{:.20}'.format(self.name)
  
  @staticmethod
  def valid_date(str):
    if re.match(r'^[0-9]{1,4}([-|/][0-9]{2,4})*([-|/][0-9]{2,4})*$', str):
      return str
    return ''

class Textbook(Bibliography):
  author = models.ManyToManyField(Author)
  texts = models.ManyToManyField(Text)
  text_creation_date = models.CharField(max_length=15)
  text_publication_date = models.CharField(max_length=15)
  SPHERE_CHOICES = (
    ('morphology', 'Ձևաբանություն'),
    ('syntax', 'Շարահյուսություն'),
    ('lexicology', 'Բառագիտություն'),
    ('linguistics', 'Տեսական լեզվաբանություն'),
  )
  sphere = models.CharField(
    max_length=25,
    choices=SPHERE_CHOICES,
    default='linguistics',
  )
  
class Fiction(Bibliography):
  text = models.ForeignKey(Text)
  genre = models.CharField(max_length=100)
  text_creation_date = models.CharField(max_length=15)
  text_publication_date = models.CharField(max_length=15)
  translation = models.ManyToManyField(Author,blank=True)
  TRANS_CHOICES = (
    ('no', 'Դատարկ'),
    ('eng', 'Անգլերեն'),
    ('ru', 'Ռուսերեն'),
    ('ge', 'Գերմաներեն'),
    ('esp', 'Իսպաներեն'),
    ('fr', 'Ֆրանսերեն'),
  )
  MEDIATION_CHOICES = (
    ('yes', 'Միջնորդված'),
    ('no', 'Չմիջնորդված'),
  )
  mediation = models.CharField(
    max_length=4,
    choices=MEDIATION_CHOICES,
    default='no',
  )
  translation_original = models.CharField(
    max_length=10,
    choices=TRANS_CHOICES,
    default='no',
  )
  translation_mediator = models.CharField(
    max_length=10,
    choices=TRANS_CHOICES,
    default='no',
  )

class Press(Bibliography):
  text = models.ForeignKey(Text)
  text_publication_date = models.CharField(max_length=15)
  number = models.IntegerField(default=0,blank=True,null=True)
  sphere = models.CharField(max_length=200)
  type = models.CharField(max_length=200)
  link = models.CharField(max_length=200,blank=True,null=True)
