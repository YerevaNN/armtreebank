from tokenization.models import Word, Cconj
from tokenization.forms import CconjForm

class CconjParser:

  def data_from_request(self, request):
    self.form = CconjForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'cconj'
    wrd.save()

    if self.form.is_valid():
      cconj = self.form.save()
      cconj.parent = wrd
      cconj.save()

  def parse_html(self):
    return '{}'.format('cconj'.upper())