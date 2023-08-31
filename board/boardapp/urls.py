from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, ReplyList, accept_reply, delete_reply
from django.conf.urls.static import static
 
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
]