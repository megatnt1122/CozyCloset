from django.urls import path
from .views import UploadView, ClosetCreateView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, deleteItem, usersClosets, openCloset, deleteCloset, AddToCloset
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
    path('clothes/', views.Clothes, name='user-clothes'),
    path('clothes/<str:itemid>/addtocloset/', views.AddToCloset, name='addto-closet'),
    path('createcloset/', ClosetCreateView.as_view(), name='create-create'),
    path('closets/', views.usersClosets, name="user-closets"),
    path('closets/<str:closetid>/', views.openCloset, name="open-closet"),
    path('closets/<str:closetid>/delete/', views.deleteCloset, name="delete-closet"),
    path('delete/<str:itemid>/', views.deleteItem, name="delete-item"),
    path('delete/<str:itemid>/<str:closetid>/', views.deleteItem, name="delete-citem")
]

# <app>/<model>_<viewtype>.html
