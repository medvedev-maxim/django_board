from django.forms import ModelForm
from .models import Post, Reply, User, UserRegisterCode
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

class BasicSignupForm(SignupForm):
  def save(self, request):
      user = super(BasicSignupForm, self).save(request)
      return user


class RegisterForm(UserCreationForm):
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Подтверждение пароля')

  class Meta:
    model = User
    fields = (
      "username",
      "email",
      "password1",
      "password2",
    )
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
      # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}), # Для паролей виджет не работает. Чтобы задать атрибуты, например, название класса, следует использовать поле модели, как показано выше.
      # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
    }

  def clean(self):
      username = self.cleaned_data.get('username')
      email = self.cleaned_data.get('email')
      if User.objects.filter(username=username).exists():
          raise forms.ValidationError("Пользователь с таким именем уже существует")
      if User.objects.filter(email=email).exists():
          raise forms.ValidationError("Пользователь с таким email уже существует")
      return super().clean()

class LoginForm(AuthenticationForm):
  class Meta:
      model = User
      fields = (
        "username",
        "password",
          )
       
class СheckingCodeForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
  code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Код')