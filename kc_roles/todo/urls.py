from django.urls import path
from .api.views import TodoListCreateView, TodoDetailView

urlpatterns = [
  path('todos/', TodoListCreateView.as_view(), name='todo_list_create'),
  path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
]

