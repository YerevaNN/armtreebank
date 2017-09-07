import json

from tokenization.models import Word, Noun, Verb

for _w in Word.objects.all():
  if len(Verb.objects.filter(parent=_w)):
    _v = Verb.objects.filter(parent=_w)[0]
    _v.delete()
    _w.delete()

with open('scripts/wiki_verbs.json', 'r+', encoding='utf-8') as file:
  content = file.read()

data = json.loads(content)

for word in data:
  first = True
  lemma = False
  
  for word_dec in word:
    wrd = Word()
    vrb = Verb()
    for a in word_dec:
      if a == 'word':
        wrd.word = word_dec[a]
      elif a == 'root':
        vrb.root = word_dec[a]
      elif a == 'form':
        vrb.type = word_dec[a]
      elif a == 'type':
        vrb.form = word_dec[a]
      elif a == 'demq':
        vrb.demq = word_dec[a]
      elif a == 'quantity':
        vrb.quantity = word_dec[a]
      elif a == 'verj':
        vrb.ending = word_dec[a]
    wrd.pos = 'verb'
    if not first:
      wrd.lemma = lemma
    wrd.save()  
    if first:
      lemma = wrd
      first = False
    vrb.parent = wrd
    vrb.save()    
