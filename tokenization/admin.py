from django.contrib import admin

from .models import Sentence, Token

admin.site.register(Sentence)
admin.site.register(Token)