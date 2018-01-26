from tokenization.models import Word, Intj
from tokenization.forms import IntjForm

class IntjParser:
  interjections = ['ծի՜վ֊ծի՜վ', 'ճը՜ռռ֊ճը՜ռռ', 'զը՜զզ', 'բը՜զզ', 'տը՜զզ', 'վը՜զզ', 'ծուղրուղո՜ւ', 'հա՛ֆ֊հա՛ֆ', 'միաո՜ւ', 'զրը՛նգ', 'չը՜խկ֊չը՜խկ', 'ո՜ւ', 'չրա՜խկ', 'չրը՛խկ', 'թը՜ռռ', 'թը՛խկ', 'թրը՛խկ', 'շը՛խկ', 'շը՛րխկ', 'ղա՜֊ղա՜', 'վա՜յ', 'վո՜ւյ', 'վա՜հ', 'օ՜յ', 'ո՜ւյ', 'օ՜հ', 'է՜հ', 'ա՜խ', 'ամա՜ն', 'ո՜ւֆ', 'ի՜ֆ', 'ա՜', 'ֆո՜ւ', 'ֆի՜', 'վա՜խ', 'ջա՜ն', 'ուխա՜յ', 'օխա՜յ', 'ֆո՜ւհ', 'փա՜հ', 'պա՜հ', 'օհո՜', 'ըհը՜', 'վա՜շ', 'վի՜շ', 'բա՜', 'վա՜', 'օ՜', 'ո՜ւխ', 'ջա՜ն', 'օխա՜յ', 'ուխա՜յ', 'վա՜յ', 'ո՜ւյ', 'օ՜հ', 'ա՜խ', 'օ՜յ', 'օհո՜', 'օ՜հ', 'բա՜', 'ա՜', 'պա՜հ', 'պա հո՜', 'վա՜', 'վա՜յ', 'վա՜հ', 'վա՜յ', 'վո՜ւյ', 'վի՜', 'վըի՜', 'ըը՜', 'վա՜շ', 'վո՜ւշ', 'վի՜շ', 'ա՜', 'ամա՜ն', 'ֆո՜ւհ', 'փո՜ւ', 'ա՜խ', 'օ՜', 'ի՜հ', 'թյո՜ւհ', 'թո՜ւհ', 'թո՜ւ', 'վա՜հ', 'ո՜ւհ', 'օ՜հ', 'է՜հ', 'ա՜հ', 'օ՜ֆ', 'ա՜խ', 'հը՜', 'ա՛յ֊ա՛յ֊ա՛յ', 'ա՛յ֊ա՛յ', 'ա՛յ', 'վա՜յ֊վա՜յ', 'ա՜խ', 'ը՜հ', 'ո՜ւհ', 'է՜խ', 'օ՜ֆ', 'էհե՜յ', 'ա՜խ', 'է՜խ', 'ավա՜ղ', 'օ՜հ', 'վա՜յ', 'վա՜խ', 'է՜', 'է՜հ', 'ա՜հ', 'ը՜հ', 'ա՛', 'ա՛յ', 'հե՜յ', 'է՜յ', 'էհե՜յ', 'հա՛յ', 'հարա՜յ', 'տո՛', 'ծո՛', 'հե՛', 'օ՜ն', 'քը՛ս֊քը՛ս', 'փի՛շտ', 'քշա՛', 'ջո՛ւ֊ջո՛ւ֊ջո՛ւ', 'բռավո՛', 'բի՛ս', 'զահրումա՜ր', 'չո՜ռ', 'զուռնա՜', 'ամմե՛ն', 'ամե՛ն', 'ապրի՛ս', 'ապրե՛ս', 'կեցցե՛ս', 'անո՜ւշ', 'բարև՛', 'համմե՜', 'մեղա՜', 'ա՛ռ']
  alphabet = ''
  
  def sync(self, drop=False):
    if drop:
      for _w in Word.objects.all():
        if len(Intj.objects.filter(parent=_w)):
          _a = Intj.objects.filter(parent=_w)[0]
          _a.delete()
          _w.delete()

    for intj in self.interjections:
      clean = ''.join(filter(lambda x: x not in '՛՜' , list(intj)))
      try:
        Word.objects.get(word=clean)
      except:
        wrd = Word()
        wrd.word = clean
        wrd.pos = 'intj'
        wrd.save()
        pnct = Intj()
        pnct.parent = wrd
        pnct.value_sym = intj
        pnct.save()

  def data_from_request(self, request):
    self.form = IntjForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'intj'
    wrd.save()

    if self.form.is_valid():
      intj = self.form.save()
      intj.parent = wrd
      intj.value_sym = ''.join(filter(lambda x: x not in '՛՜' , self.post.get('word')))
      intj.save()

  def parse_html(self):
    return '{}'.format('intj'.upper())
      

