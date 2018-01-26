from tokenization.models import Word, Aux
from tokenization.forms import AuxForm

class AuxParser:

  def data_from_request(self, request):
    self.form = AuxForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'aux'
    wrd.save()

    if self.form.is_valid():
      aux = self.form.save()
      aux.parent = wrd
      aux.save()

  def parse_html(self):
    return '{}'.format('aux'.upper())