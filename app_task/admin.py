from django.contrib import admin
from .models import *


class ItemsAdmin(admin.ModelAdmin):
    list_display = ['id', ]
admin.site.register(Items, ItemsAdmin)
