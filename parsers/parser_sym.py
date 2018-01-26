from tokenization.models import Word, Sym

class SymParser:

  def data_from_request(self, request):
    self.post = request.POST

  def save(self):
    wrd = Word()
    wrd.word = self.post.get('word')
    wrd.pos = 'sym'
    wrd.save()

    sym = Sym()
    sym.parent = wrd
    sym.save()

  def parse_html(self):
    return '{}'.format('sym'.upper())