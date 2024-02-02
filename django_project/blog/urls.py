from django.urls import path
from .views import UploadView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, deleteItem
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('list/', views.list, name='list'),
    path('closet/', views.closet, name='user-closet'),
    path('closet/<str:itemid>/delete/', views.deleteItem, name="delete-item")
]

# <app>/<model>_<viewtype>.html
