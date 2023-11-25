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

    path('add_moderator_request/<int:user_id>/<int:group_id>/', views.add_moderator_request, name='add_moderator_request'),
    path('approve_moderator/<int:user_id>/<int:group_id>/', views.approve_moderator_request, name='approve_moderator'),
    path('reject_moderator/<int:user_id>/<int:group_id>/', views.reject_moderator_request, name='reject_moderator'),
    path('delete_moderator/<int:user_id>/<int:group_id>/', views.delete_moderator, name='delete_moderator'),

    
] 
