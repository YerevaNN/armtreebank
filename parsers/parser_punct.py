from tokenization.models import Word, Punct

class PunctParser:
  punctuations = {
    ('՚','\u055A'),
    ('՛','\u055B'),
    ('՜','\u055C'),
    ('՞','\u055E'),
    ('՟','\u055F'),
    ('`',''),
    ('֊',''),
    ('՚',''),
    ('«',''),
    ('»',''),
    ('(',''),
    (')',''),
    ('[',''),
    (']',''),
    ('{',''),
    ('}',''),
    (',',''),
    ('.',''),
    ('-',''),
    ('—',''),
    (':',''),
    ('...',''),
    ('....',''),
  }
  
  def sync(self, drop=False):
    if drop:
      for _w in Word.objects.all():
        if len(Punct.objects.filter(parent=_w)):
          _a = Punct.objects.filter(parent=_w)[0]
          _a.delete()
          _w.delete()

    for u_p, _ in self.punctuations:
      wrd = Word()
      wrd.word = u_p
      wrd.pos = 'punct'
      wrd.save()
      pnct = Punct()
      pnct.parent = wrd
      pnct.save()
      
  def data_from_request(self, request):
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'punct'
    wrd.save()

    punct = Punct()
    punct.parent = wrd
    punct.save()

  def parse_html(self):
    return '{}'.format('num'.upper())