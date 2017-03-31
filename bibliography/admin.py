from django.contrib import admin
from .models import Author, Text, Textbook, Fiction, Press

admin.site.register(Author)
admin.site.register(Text)
admin.site.register(Textbook)
admin.site.register(Fiction)
admin.site.register(Press)