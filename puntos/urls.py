from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('entradas/', views.entrada_list, name='entrada_list'),
    path('entradas/create/', views.entrada_create, name='entrada_create'),
    path('entradas/update/<int:pk>/', views.entrada_update, name='entrada_update'),
    path('entradas/delete/<int:pk>/', views.entrada_delete, name='entrada_delete'),
]
