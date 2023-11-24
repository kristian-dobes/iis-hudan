from django.urls import path, include
from . import views

app_name = "groups"

urlpatterns = [
    path('<int:group_id>/', views.detail, name='detail'),
    path('edit/<int:group_id>/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('<int:group_id>/threads/', include("threads.urls", namespace="threads")),
     path('list_groups/', views.list_groups, name='list_groups'),
    path('<int:group_id>/delete_group', views.delete_group, name='delete_group'),
]
