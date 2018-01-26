from tokenization.models import Word, Numeral
from tokenization.forms import NumeralForm

class NumParser:

  def data_from_request(self, request):
    self.form = NumeralForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'num'
    wrd.save()

    if self.form.is_valid():
      num = self.form.save()
      num.parent = wrd
      num.save()

  def parse_html(self):
    return '{}'.format('num'.upper())