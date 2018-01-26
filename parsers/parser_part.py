from tokenization.models import Word, Part
from tokenization.forms import PartForm

class PartParser:

  def data_from_request(self, request):
    self.form = PartForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'part'
    wrd.save()

    if self.form.is_valid():
      part = self.form.save()
      part.parent = wrd
      part.save()

  def parse_html(self):
    return '{}'.format('part'.upper())