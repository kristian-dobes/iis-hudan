from django.urls import path, include
from . import views

app_name = "groups"

urlpatterns = [
    path('<int:group_id>/', views.detail, name='detail'),
    path('edit/<int:group_id>/', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('<int:group_id>/threads/', include("threads.urls", namespace="threads")),
]
