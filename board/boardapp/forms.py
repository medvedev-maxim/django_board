from django.forms import ModelForm
from .models import Post, Reply
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(ModelForm):
  content = forms.CharField(widget=SummernoteWidget(), label='Текст')
  
  class Meta:
    model = Post
    fields = ['categoryType','title','content']
    # fields = ['categoryType','title','content']
    widgets = {
        'categoryType' : forms.Select(attrs={'class': 'form-control',}),
        'title' : forms.TextInput(attrs={'type': 'text', 'class': 'form-control', }),
        # 'content' : forms.Textarea(attrs={'class': 'form-control',})
    }
    labels = {
      'categoryType': 'Категория объявления',
      'title': 'Заголовок объявления',
    }

class ReplyForm(ModelForm):
  class Meta:
    model = Reply
    fields = ['text']
    widgets = {
        'text' : forms.Textarea(attrs={'class': 'form-control',})
    }
    labels = {
      'text': 'Введите текст отклика',
    }