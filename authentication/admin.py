from django.contrib import admin
from .models import *


class UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'password']
admin.site.register(User, UsersAdmin)