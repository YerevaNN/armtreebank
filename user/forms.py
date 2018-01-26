from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(label='Username', max_length=256)
  password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=256)
