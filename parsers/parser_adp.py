from tokenization.models import Word, Adp
from tokenization.forms import AdpForm

class AdpParser: 
  def sync(self):
    pass
  
  def data_from_request(self, request):
    self.form = AdpForm(request.POST)
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'adp'
    wrd.save()

    if self.form.is_valid():
      adp = self.form.save()
      adp.parent = wrd
      adp.save()

  def parse_html(self):
    return '{}'.format('adp'.upper())
  
