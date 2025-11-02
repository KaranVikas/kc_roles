from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerOrParent
from ..models import Todo
from .serialziers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

# List and Create Todos
class TodoListCreateView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    """
      Students: See only their own todos
      Parents: See their children's todos
      Admin: See all todos
    """

    user = request.user
    if user.user_type == 'admin':
      todos = Todo.objects.all()
    elif user.user_type == 'parent':
      #Get todos of all children + own todos
      children_ids = user.children.values_list('user_id', flat=True)
      todos = Todo.objects.filter(user_id__in=children_ids) | Todo.objects.filter(user=user)
    else:
      todos = Todo.objects.filter(user=user)
    todos = todos.order_by('-created_at')
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete Todo by ID
class TodoDetailView(APIView):
  permission_classes = [IsAuthenticated, IsOwnerOrParent]

  def get_object(self, pk):
    obj = get_object_or_404(Todo, pk=pk)
    self.check_object_permissions(self.request, obj)
    return obj

  def get(self, request, pk):
    todo = self.get_object(pk)
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    todo = self.get_object(pk)
    serializer = TodoSerializer(todo, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    todo = self.get_object(pk=pk)
    todo.delete()
    return Response({'message':'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

