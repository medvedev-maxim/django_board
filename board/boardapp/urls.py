from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, ReplyList, accept_reply, delete_reply, AddReplySuccess, LoginView, LogoutView, RegisterView
from django.conf.urls.static import static
# from django.contrib.auth.views import LoginView, LogoutView, RegisterView
 
urlpatterns = [
    path('', PostList.as_view(), name='posts_start'),
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('replys/', ReplyList.as_view(), name='reply_list'),
    path('replys/delete/<int:pk>/', delete_reply, name='delete_reply'),
    path('replys/accept/<int:pk>/', accept_reply, name='accept_reply'),
    path('add_reply_success/', AddReplySuccess.as_view(), name='add_reply_success'),
    path('sign/', LoginView.as_view(template_name='boardapp/login.html'), name='sign'),
    path('logout/', LogoutView.as_view(template_name='boardapp/logout.html'), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup')
]