from tokenization.models import Word, X
from tokenization.forms import XForm

class XParser:

  def data_from_request(self, request):
    self.form = XForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'x'
    wrd.save()

    if self.form.is_valid():
      x = self.form.save()
      x.parent = wrd
      x.save()

  def parse_html(self):
    return '{}'.format('x'.upper())