from django.contrib import admin
from .models import Post, Reply
from django_summernote.admin import SummernoteModelAdmin

# admin.site.register(Post)
admin.site.register(Reply)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)