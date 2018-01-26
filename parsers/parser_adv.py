import os

import csv

from tokenization.models import Word, Adv
from tokenization.forms import AdvForm

class AdvParser:
  def sync(self, drop=False):
    if drop:
      for _w in Word.objects.all():
        if len(Adv.objects.filter(parent=_w)):
          _a = Adv.objects.filter(parent=_w)[0]
          _a.delete()
          _w.delete()

    dir_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(dir_path, '../','sync/hy_adj_adv.csv')

    with open(csv_path, 'r+', encoding='utf-8') as in_file:
      csvreader = csv.reader(in_file, delimiter=',')
      for row in csvreader:
        if isinstance(row, list) and len(row) == 2:
          wrd = Word()
          wrd.word = row[0]
          wrd.pos = 'adv'
          wrd.save()

          adv = Adv()
          adv.parent = wrd
          adv.lemma = row[0]
          adv.save()

  def data_from_csv(self, word):
    self.word = word.strip()
  
  def data_from_request(self, request):
    self.form = AdvForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'adv'
    wrd.save()

    if self.form.is_valid():
      adv = self.form.save()
      adv.parent = wrd
      adv.save()

  def parse_html(self):
    return '{}'.format('adv'.upper())
  
