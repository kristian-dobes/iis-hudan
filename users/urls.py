from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path('<int:user_id>/', views.detail, name='detail'),
    path('list_users/', views.list_users, name='list_users'),
    path('<int:user_id>/delete_user', views.delete_user, name='delete_user'),
    path('edit/<int:user_id>/', views.edit, name='edit'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),
]
