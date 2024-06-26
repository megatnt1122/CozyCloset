from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('market/', include('core.urls')),
    path('items/', include('item.urls')),
    path('inbox/', include('conversation.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tutorial/', views.about, name='tutorial'),
    path('upload/', UploadView.as_view(), name='upload'),
    path('list/', views.list, name='list'),
    path('createcloset/', ClosetCreateView.as_view(), name='create-create'),
    path('myclosets/', views.myClosets, name="my-closets"),
    path('myclosets/<str:closetid>/', views.openMyCloset, name="open-closet"),
    path('myclosets/<str:closetid>/createoutfit/', views.createOutfit, name='create-outfit'),
    path('myclosets/<str:outfitid>/deleteoutfit/', views.deleteOutfit, name='delete-outfit'),
    path('myclosets/<int:closetid>/edit/', ClosetUpdateView.as_view(), name='closet-edit'),
    path('myclosets/<str:closetid>/delete/', views.deleteCloset, name="delete-closet"),
    path('myclosets/<str:closetid>/remove/<str:itemid>/', views.deleteItem, name="delete-citem"),
    path('<str:username>/closets/', views.userClosets, name="user-closets"),
    path('<str:username>/closets/<str:closetname>/', views.openUserCloset, name="open-usercloset"),
    path('clothes/', views.Clothes, name='my-clothes'),
    path('clothes/delete/<str:itemid>/', views.deleteItem, name="delete-item"),
    path('clothes/<str:itemid>/addtocloset/', views.AddToCloset, name='addto-closet'),
    path('clothes/<str:itemid>/addtopost/', views.createPost, name='addto-post'),
    path('view-outfits/', views.view_outfits, name='view-outfits'),
    path('search/', SearchView.as_view(), name='user-search'),
    path('follow/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<str:username>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('dm/', views.dm, name='dm'),
    path('dm/<int:pk>', views.detailM, name='view-message'),
    path('dm/new/<int:user_pk>', views.new_message, name='send-message'),
    path('like/<int:pk>', LikeView, name="like_post"),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('comments/<int:comment_id>/like/', views.CommentLikeView, name='comment_like'),
    path('comments/<int:commentid>/delete/', views.deleteComment, name='comment-delete'),
    path('<str:username>/', views.userProfile, name='user-profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# <app>/<model>_<viewtype>.html
