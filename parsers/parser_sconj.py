from tokenization.models import Word, Sconj
from tokenization.forms import SconjForm

class SconjParser:

  def data_from_request(self, request):
    self.form = SconjForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'sconj'
    wrd.save()

    if self.form.is_valid():
      sconj = self.form.save()
      sconj.parent = wrd
      sconj.save()

  def parse_html(self):
    return '{}'.format('sconj'.upper())