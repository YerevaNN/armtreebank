from tokenization.models import *

class DefaultParser:
  def __init__(self, parser_cls):
  	self.parser_cls = parser_cls

  def data_from_request(self, request):
  	self.word = request.POST.get('word')

  def save(self):
    pass
    '''
    wrd = Word()
    wrd.word = self.word
    wrd.pos = self.parser_cls.POS
    wrd.save()
    pnct = self.parser_cls()
    pnct.parent = wrd
    pnct.save()'''

  def parse_html(self):
  	return '{} - {}'.format(self.parser_cls.POS.upper(), self.word)