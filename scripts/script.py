import csv

from tokenization.models import Noun, Word
from tokenization.parser_noun import NounParserFactory

for _w in Word.objects.all():
  if len(Noun.objects.filter(parent=_w)):
    _v = Noun.objects.filter(parent=_w)[0]
    _v.delete()
    _w.delete()
    print('Deleted..')

with open('scripts/en_nouns.csv', 'r+', encoding='utf-8') as in_file:
  csvreader = csv.reader(in_file, delimiter=',')
  n = 0
  for row in csvreader:
    if isinstance(row, list) and len(row) == 2:
      attr = row[1].split('~')
      for a in attr:
        try:
          p = NounParserFactory.parser(row[0], a)
          p.save()
          n += 1
          print('Saved: ', n)
        except Exception:
          pass