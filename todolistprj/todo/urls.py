from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, CustomLoginView, RegisterationView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    
    path('', TaskListView.as_view(), name='task-list'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('register/', RegisterationView.as_view( ), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
]




