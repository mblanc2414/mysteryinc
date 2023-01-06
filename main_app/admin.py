from django.contrib import admin
from .models import Character, Unmasked, Photo
# Register your models here.
admin.site.register(Character)

admin.site.register(Unmasked)

admin.site.register(Photo)