from tokenization.models import Word, Det
from tokenization.forms import DetForm

class DetParser: 
  def sync(self):
    pass
  
  def data_from_request(self, request):
    self.form = DetForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'det'
    wrd.save()

    if self.form.is_valid():
      det = self.form.save()
      det.parent = wrd
      det.save()

  def parse_html(self):
    return '{}'.format('det'.upper())
  
