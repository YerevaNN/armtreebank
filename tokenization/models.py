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
  
  def __str__(self):
    return '{t}'.format(t=self.token)