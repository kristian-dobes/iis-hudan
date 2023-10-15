from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path('<int:group_id>/', views.detail, name='detail'),
    path('edit/', views.edit, name='edit'),
    path('create/', views.create, name='create')
]
