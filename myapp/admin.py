from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User, EventInfo

# Register your models here.
class EventInfoAdmin(admin.ModelAdmin):
    list_display = ['event_date', 'host', 'venue']


class PostAdmin(admin.ModelAdmin):
    list_filter = ['published_date']
    list_display = ['title', 'author', 'published_date']



admin.site.register(Post, PostAdmin)
admin.site.register(EventInfo, EventInfoAdmin)
admin.site.register(User, UserAdmin)
