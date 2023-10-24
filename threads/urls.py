from django.urls import path
from . import views

app_name = "threads"

urlpatterns = [
    path('<int:thread_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:thread_id>/post/', views.post, name='post'),
    path('<int:thread_id>/post/<int:post_id>/like', views.like, name='like'),
]
