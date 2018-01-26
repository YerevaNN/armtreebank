import os

import csv

from tokenization.models import Word, Adj
from tokenization.forms import AdjForm

class AdjParser:
  def sync(self, drop=False):
    if drop:
      for _w in Word.objects.all():
        if len(Adj.objects.filter(parent=_w)):
          _a = Adj.objects.filter(parent=_w)[0]
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
          wrd.pos = 'adj'
          wrd.save()

          adj = Adj()
          adj.parent = wrd
          adj.lemma = row[0]
          adj.save()

  def data_from_csv(self, word):
    self.word = word.strip()

  def data_from_request(self, request):
    self.form = AdjForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'adj'
    wrd.save()

    if self.form.is_valid():
      adj = self.form.save()
      adj.parent = wrd
      adj.save()

  def parse_html(self):
    return '{}'.format('adj'.upper())
  
