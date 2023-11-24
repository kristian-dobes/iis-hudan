from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path('<int:user_id>/', views.detail, name='detail'),
    path('edit/<int:user_id>/', views.edit, name='edit'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),
]
