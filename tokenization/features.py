from django.db import models

lemma = models.CharField(max_length=250, null=True, blank=True)

abbr = models.BooleanField(default=False)
adp_type = models.CharField(
  max_length=7,
  choices=(('prep', 'Prep'),
           ('post', 'Post'),
           ('comadp', 'Comadp'),
          ),
  blank=True,
)
animacy = models.ManyToManyField('tokenization.NounAnimacy', blank=True)
aspect = models.CharField(
  max_length=7,
  choices=(('dur', 'Dur'),
           ('imp', 'Imp'),
           ('iter', 'Iter'),
           ('perf', 'Perf'),
           ('prosp', 'Prosp'),
          ),
  blank=True,
)
case = models.CharField(
  max_length=15,
  choices=(('nom', 'Nominative'),
           ('dat', 'Dative'),
           ('gen', 'Genitive'),
           ('abl', 'Ablative'),
           ('ins', 'Instrumental'),
           ('loc', 'Locative'),
          ),
  blank=True,
)
conj_type = models.CharField(
  max_length=6,
  choices=(('oper', 'Oper'),
           ('comp', 'Comp'),
          ),
  blank=True,
)
definite = models.CharField(
  max_length=6,
  choices=(('def', 'Def'),
           ('indef', 'Indef'),
          ),
  blank=True,
)
degree = models.CharField(
  max_length=4,
  choices=(('pos', 'Positive'),
           ('cmp', 'Comparative'),
           ('sup', 'Superlative'),
           ('abs', 'Absolute superlative'),
          ),
  blank=True,
)
echo = models.CharField(
  max_length=4,
  choices=(('ech', 'Echo'),
           ('rdp', 'Reduplicative'),
          ),
  blank=True,
)
foreign = models.BooleanField(default=False)
hyph = models.BooleanField(default=False)
mood = models.CharField(
  max_length=4,
  choices=(('cnd', 'Conditional'),
           ('imp', 'Imperative'),
           ('ind', 'Indicative'),
           ('nec', 'Necessitative'),
           ('sub', 'Subjunctive'),
          ),
  blank=True,
)
name_type = models.CharField(
  max_length=4,
  choices=(('com', 'Com'),
           ('geo', 'Geo'),
           ('giv', 'Giv'),
           ('oth', 'Oth'),
           ('pro', 'Pro'),
           ('prs', 'Prs'),
           ('sur', 'Sur'),
          ),
  blank=True,
)
num_form = models.CharField(
  max_length=10,
  choices=(('armenian', 'Armenian'),
           ('digit', 'Digit'),
           ('roman', 'Roman'),
           ('word', 'Word'),
          ),
  blank=True,
)
num_type = models.CharField(
  max_length=7,
  choices=(('card', 'Card'),
           ('dist', 'Dist'),
           ('frac', 'Frac'),
           ('ord', 'Ord'),
           ('range', 'Range'),
          ),
  blank=True,
)
number = models.CharField(
  max_length=13,
  choices=(('sing', 'Singular'),
           ('plur', 'Plural'),
           ('coll', 'Collective'),
           ('assoc', 'Associative'),
          ),
  blank=True,
)
person = models.CharField(
  max_length=3,
  choices=(('1', '1'),
           ('2', '2'),
           ('3', '3'),
          ),
  blank=True,
)
polarity = models.CharField(
  max_length=4,
  choices=(('neg', 'Neg'),
           ('pos', 'Pos'),
          ),
  blank=True,
)
poss = models.BooleanField(default=False)
poss_number = models.CharField(
  max_length=5,
  choices=(('sing', 'Sing'),
           ('plur', 'Plur'),
          ),
  blank=True,
)
poss_person = models.CharField(
  max_length=3,
  choices=(('1', '1'),
           ('2', '2'),
           ('3', '3'),
          ),
  blank=True,
)
pron_type = models.CharField(
  max_length=5,
  choices=(('art', 'Art'),
           ('dem', 'Dem'),
           ('emp', 'Emp'),
           ('ind', 'Ind'),
           ('int', 'Int'),
           ('neg', 'Neg'),
           ('prs', 'Prs'),
           ('rcp', 'Rcp'),
           ('rel', 'Rel'),
           ('tot', 'Tot'),
          ),
  blank=True,
)
reflex = models.BooleanField(default=False)
subcat = models.CharField(
  max_length=5,
  choices=(('intr', 'Intransitive'),
           ('tran', 'Transitive'),
          ),
  blank=True,
)
tense = models.CharField(
  max_length=5,
  choices=(('imp', 'Imp'),
           ('past', 'Past'),
           ('pres', 'Pres'),
          ),
  blank=True,
)
verb_form = models.CharField(
  max_length=5,
  choices=(('conv', 'Conv'),
           ('fin', 'Fin'),
           ('inf', 'Inf'),
           ('part', 'Part'),
          ),
  blank=True,
)
voice = models.CharField(
  max_length=5,
  choices=(('act', 'Act'),
           ('cau', 'Cau'),
           ('mid', 'Mid'),
           ('pass', 'Pass'),
          ),
  blank=True,
)
materiality = models.CharField(
  max_length=5,
  choices=(('conc', 'concrete'),
           ('astr', 'abstract'),
          ),
  blank=True,
)
nominalized = models.BooleanField(default=False)