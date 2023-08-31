from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView
 
urlpatterns = [
    path('', PostList.as_view(), name='posts_start'),
    path('posts/', PostList.as_view(), name='posts_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

]