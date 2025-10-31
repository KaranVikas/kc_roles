from django.shortcuts import render, get_object_or_404
from ..models import Todo
from .serialziers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

# List and Create Todos
class TodoListCreateView(APIView):
  def get(self, request):
    todos = Todo.objects.all().order_by('-id')
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
  def get(self, request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    serializer = TodoSerializer(todo)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
