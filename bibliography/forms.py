from django.forms import ModelForm
from .models import Author, Text, Textbook, Fiction, Press

class AuthorForm(ModelForm):
  class Meta:
    model = Author
    fields = '__all__'
    
class TextForm(ModelForm):
  class Meta:
    model = Text
    fields = '__all__'
    
class TextbookForm(ModelForm):
  class Meta:
    model = Textbook
    fields = '__all__'
    
class FictionForm(ModelForm):
  class Meta:
    model = Fiction
    fields = '__all__'
    
class PressForm(ModelForm):
  class Meta:
    model = Press
    fields = '__all__'
