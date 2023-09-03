from django.contrib import admin
from .models import Post, Reply, UserRegisterCode
from django_summernote.admin import SummernoteModelAdmin

# admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(UserRegisterCode)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)