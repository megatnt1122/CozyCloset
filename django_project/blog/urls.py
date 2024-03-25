from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('market/', include('core.urls')),
    path('items/', include('item.urls')),
    path('inbox/', include('conversation.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('list/', views.list, name='list'),
    path('createcloset/', ClosetCreateView.as_view(), name='create-create'),
    path('myclosets/', views.myClosets, name="my-closets"),
    path('myclosets/<str:closetid>/', views.openMyCloset, name="open-closet"),
    path('myclosets/<int:closetid>/edit/', ClosetUpdateView.as_view(), name='closet-edit'),
    path('myclosets/<str:closetid>/delete/', views.deleteCloset, name="delete-closet"),
    path('<str:username>/closets/', views.userClosets, name="user-closets"),
    path('<str:username>/closets/<str:closetname>/', views.openUserCloset, name="open-usercloset"),
    path('delete/<str:itemid>/', views.deleteItem, name="delete-item"),
    path('delete/<str:itemid>/<str:closetid>/', views.deleteItem, name="delete-citem"),
    path('clothes/', views.Clothes, name='my-clothes'),
    path('clothes/<str:itemid>/addtocloset/', views.AddToCloset, name='addto-closet'),
    path('clothes/<str:itemid>/addtopost/', PostCreateView.as_view(), name='addto-post'),
    path('createoutfit/', views.createOutfit, name='create-outfit'),
    path('search/', SearchView.as_view(), name='user-search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# <app>/<model>_<viewtype>.html
