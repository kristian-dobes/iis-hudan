from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('<int:user_id>/', views.detail, name='detail'),
    path('edit/', views.edit, name='edit'),
    path('list_users/', views.list_users, name='list_users'),
    path('<int:user_id>/delete_user', views.delete_user, name='delete_user'),
]
