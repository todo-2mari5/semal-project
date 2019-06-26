from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_filter = ['published_date']
    list_display = ['title', 'author', 'published_date']



admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
