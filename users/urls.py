from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('<int:user_id>/', views.detail, name='detail'),
    path('edit/', views.edit, name='edit'),
]
