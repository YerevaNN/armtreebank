from tokenization.models import Word, Pron
from tokenization.forms import PronForm

class PronParser:
  def sync(self):
    pass
  
  def data_from_request(self, request):
    self.form = PronForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'pron'
    wrd.save()

    if self.form.is_valid():
      pron = self.form.save()
      pron.parent = wrd
      pron.save()

  def parse_html(self):
    return '{}'.format('pron'.upper())
      

