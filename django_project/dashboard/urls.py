from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('market/', views.index, name='index'),
]