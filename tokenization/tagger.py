import re
from itertools import chain

from tokenization.models import Word

class Tagger:
  def __init__(self, word):
    self.word = word.strip()
  def tag(self):
    try:
      res = Word.objects.filter(word=self.word)
      lower_res = Word.objects.filter(word=self.word.lower())
      upper_res = Word.objects.filter(word=self.word.upper())
      title_res = Word.objects.filter(word=self.word.title())
    except:
      return False
    else:
      return list(chain(res, lower_res, upper_res, title_res))
    