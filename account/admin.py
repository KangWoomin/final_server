from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['userID','email','name']
    list_display_links = ['userID','email','name']
    search_fields = ['name']

admin.site.register(User, UserAdmin)
