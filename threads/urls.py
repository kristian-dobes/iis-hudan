from django.urls import path
from . import views

app_name = "threads"

urlpatterns = [
    path('<int:thread_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:thread_id>/post/', views.post, name='post'),
    path('<int:thread_id>/post/<int:post_id>/like', views.like, name='like'),
    path('delete_post<int:thread_id>/<int:post_id>', views.delete_post, name='delete_post'),
    path('edit_thread/<int:thread_id>', views.edit_thread, name='edit_thread'),
    path('delete_thread/<int:thread_id>/', views.delete_thread, name='delete_thread'),
    
]
