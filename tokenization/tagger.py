import re

from tokenization.models import Word

class Tagger:
  def __init__(self, word):
    self.word = word
  
  def tag(self):
    try:
      res = Word.objects.filter(word=self.word)
    except:
      return False
    else:
      return res
    