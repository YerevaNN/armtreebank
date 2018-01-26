from parsers.parser_noun import NounParserFactory
from parsers.parser_verb import VerbParserFactory
from parsers.parser_adv import AdvParser
from parsers.parser_adj import AdjParser
from parsers.parser_intj import IntjParser
from parsers.parser_punct import PunctParser

from tokenization.models import NounAnimacy

#punct = PunctParser()
#punct.sync(True)

#intj = IntjParser()
#intj.sync(True)

adj = AdjParser()
adj.sync(True)

adv = AdvParser()
adv.sync(True)

animacy = ['animate', 'inanimate', 'human']
for a in animacy:
  if len(NounAnimacy.objects.filter(value=a)) == 0:
    noun_an = NounAnimacy()
    noun_an.value = a
    noun_an.title = a.upper()
    noun_an.save()

noun = NounParserFactory()
noun.sync(True)

verb = VerbParserFactory()
verb.sync(True)
