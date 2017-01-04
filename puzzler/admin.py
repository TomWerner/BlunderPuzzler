from django.contrib import admin
from .models import *


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    fields = (
        'link',
        'severity',
    )
    list_display = ('link', 'severity')
