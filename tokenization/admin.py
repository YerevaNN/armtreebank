from django.contrib import admin

from .models import Sentence, Token, Word, Noun, Verb

admin.site.register(Sentence)
admin.site.register(Token)
admin.site.register(Word)
admin.site.register(Noun)
admin.site.register(Verb)