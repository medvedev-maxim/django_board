from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Reply
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from .filters import PostFilter, ReplyFilter
from .forms import PostForm, ReplyForm
from django.urls import reverse_lazy, reverse

class PostList(ListView):
    model = Post
    template_name='boardapp/postlist.html'
    context_object_name='posts'
    # queryset = Post.objects.order_by('-dateCreation')
    ordering = ['-dateCreation'] # сортировка с помощью дженерика
    paginate_by = 10
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
    
class ReplyList(ListView):
    model = Reply
    template_name='boardapp/replylist.html'
    context_object_name='replys'
    ordering = ['-dateCreation']
    paginate_by = 10
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    
    def get_queryset(self):
        user = self.request.user
        return Reply.objects.filter(feedbackPost__user=user)
    
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ReplyFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context

# class PostDetail(DetailView):
#     model = Post
#     template_name='boardapp/postdetail.html'
#     context_object_name='post'

class PostDetail(FormView, DetailView):
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
        return super().form_valid(form)


class PostCreateView(CreateView):
    template_name = 'boardapp/postcreate.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    template_name = 'boardapp/postcreate.html'
    form_class = PostForm
    success_url = '/'
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
   
class PostDeleteView(DeleteView):
    template_name = 'boardapp/postdelete.html'
    queryset = Post.objects.all()
    success_url = '/'

def accept_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.accept()
    reply.save()
    return redirect('reply_list')

def delete_reply(request, pk):
    reply = Reply.objects.get(pk=pk)
    reply.delete()
    return redirect('reply_list')