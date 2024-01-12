from django.urls import path

from . import views

urlpatterns = [
#path("<int:id>", views.index, name="index"),
path("", views.home, name="home"),
path('upload/', views.upload, name="upload"),
path('home/', views.home, name="home"),
]