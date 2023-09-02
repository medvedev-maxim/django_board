from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Reply
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from .filters import PostFilter, ReplyFilter
from .forms import PostForm, ReplyForm
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver


class PostList(ListView):
    model = Post
    template_name='boardapp/postlist.html'
    context_object_name='posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation'] # сортировка с помощью дженерика
    paginate_by = 10

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    # def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
    #     return context
    
    # Совмещение фильтрации и пагинации
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        filtered_posts = context['filter'].qs
        paginator = Paginator(filtered_posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context
    
class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    template_name='boardapp/replylist.html'
    context_object_name='replys'
    ordering = ['-dateCreation']
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        return Reply.objects.filter(feedbackPost__user=user).order_by('-dateCreation')
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset())
    #     filtered_reply = context['filter'].qs
    #     paginator = Paginator(filtered_reply, self.paginate_by)
    #     page = self.request.GET.get('page')
    #     try:
    #         reply = paginator.page(page)
    #     except PageNotAnInteger:
    #         reply = paginator.page(1)
    #     except EmptyPage:
    #         reply = paginator.page(paginator.num_pages)
    #     context['reply'] = reply
    #     return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(LoginRequiredMixin, FormView, DetailView):
    model = Post
    form_class = ReplyForm
    template_name='boardapp/postdetail.html'
    context_object_name='post'
    # success_url = reverse_lazy('success')
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context  
    
    def form_valid(self, form):
        form.instance.feedbackUser = self.request.user
        form.instance.feedbackPost = self.get_object()
        form.save()

        # Отправка письма из вьюхи, заменена на сигнал
        # print('ПРОВЕРКА','\n',self.request.META)
        # send_mail( 
        #     subject=f'{self.request.user} оставил отклик на объявление "{form.instance.feedbackPost.title}"',
        #     message=f'"{self.request.POST["text"]}"\n\nОбработайте этот отклик и проверьте другие в разделе http://{self.request.META["HTTP_HOST"]}/replys/',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[form.instance.feedbackPost.user.email]
        # )
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'boardapp/postcreate.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'boardapp/postcreate.html'
    form_class = PostForm
    success_url = '/'
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
   
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'boardapp/postdelete.html'
    queryset = Post.objects.all()
    success_url = '/'
    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтрация объектов только для текущего пользователя
        queryset = queryset.filter(author=self.request.user)
        return queryset


def accept_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.accept()
    reply.save()

    # print('ПРОВЕРКА','\n',request,'\n', pk)
    # Отправка письма из вьюхи, заменена на сигнал  
    # send_mail( 
    #     subject=f'Ваш отклик на "{reply.feedbackPost.title}" ОДОБРЕН!',
    #     message=f'Ваш отклик "{reply.text}" был ОДОБРЕН!\nСвяжитесь с автором объявления по адресу {reply.feedbackPost.user.email}',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[reply.feedbackUser.email]
    # )  
    
    return redirect('reply_list')

def delete_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.delete()
    
    # Отправка письма из вьюхи, заменена на сигнал  
    # send_mail( 
    #     subject=f'Ваш отклик на "{reply.feedbackPost.title}" ОТКЛОНЕН!',
    #     message=f'Ваш отклик "{reply.text}" был ОТКЛОНЕН и УДАЛЕН!\nПопробуйте предложенить другой вариант',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[reply.feedbackUser.email]
    # )  
    
    return redirect('reply_list')