from django.contrib import admin
from . models import Snippet,User

# Register your models here.
admin.site.register(User)
admin.site.register(Snippet)
