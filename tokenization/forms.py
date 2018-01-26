from django.forms import ModelForm, ChoiceField

from .models import *

class VerbParserForm(ModelForm):
  class Meta:
    model = Verb
    exclude = ['POS', 'parent', 'verb_form', 'aspect', 'mood', 'person', 'polarity', 'tense', 'voice_feat', 'lemma']

class VerbManualForm(ModelForm):
  class Meta:
    model = Verb
    exclude = ['POS', 'parent', 'number', 'poss_number', 'poss_person', 'subcat', 'voice', 'abbr', 'foreign', 'echo', 'poss']

class VerbSaveForm(ModelForm):
  class Meta:
    model = Verb
    exclude = ['POS', 'parent']

class NounParserForm(ModelForm):
  class Meta:
    model = Noun
    exclude = ['POS', 'parent', 'case', 'definite', 'number', 'poss_number', 'poss_person', 'lemma']

class NounManualForm(ModelForm):
  class Meta:
    model = Noun
    exclude = ['POS', 'parent', 'animacy', 'proper', 'materiality', 'nominalized', 'abbr', 'foreign', 'echo', 'poss']

class NounSaveForm(ModelForm):
  class Meta:
    model = Noun
    exclude = ['POS', 'parent']

class SconjForm(ModelForm):
  class Meta:
    model = Sconj
    exclude = ['POS', 'parent']
    
class CconjForm(ModelForm):
  class Meta:
    model = Cconj
    exclude = ['POS', 'parent']
    
class NumeralForm(ModelForm):
  class Meta:
    model = Numeral
    exclude = ['POS', 'parent']
    
class PartForm(ModelForm):
  class Meta:
    model = Part
    exclude = ['POS', 'parent']
    
class PronForm(ModelForm):
  class Meta:
    model = Pron
    exclude = ['POS', 'parent']
    
class AuxForm(ModelForm):
  class Meta:
    model = Aux
    exclude = ['POS', 'parent']
    
class AdpForm(ModelForm):
  class Meta:
    model = Adp
    exclude = ['POS', 'parent']
    
class DetForm(ModelForm):
  class Meta:
    model = Det
    exclude = ['POS', 'parent']
    
class IntjForm(ModelForm):
  class Meta:
    model = Intj
    exclude = ['POS', 'parent', 'value_sym']
    
class AdvForm(ModelForm):
  class Meta:
    model = Adv
    exclude = ['POS', 'parent']
    
class AdjForm(ModelForm):
  class Meta:
    model = Adj
    exclude = ['POS', 'parent']

class XForm(ModelForm):
  class Meta:
    model = X
    exclude = ['POS', 'parent']

class SymForm(ModelForm):
  class Meta:
    model = Sym
    exclude = ['POS', 'parent']

class PunctForm(ModelForm):
  class Meta:
    model = Punct
    exclude = ['POS', 'parent']
    
FEATURE_FORMS = [SconjForm,
                 CconjForm,
                 NumeralForm,
                 PartForm,
                 PronForm,
                 AuxForm,
                 AdpForm,
                 DetForm,
                 IntjForm,
                 AdvForm,
                 AdjForm,
                 XForm,
                 SymForm,
                 PunctForm,
                 ]