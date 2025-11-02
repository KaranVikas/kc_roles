from rest_framework import serializers
from ..models import Todo

class TodoSerializer(serializers.ModelSerializer):
  user_name = serializers.CharField(source='user.username', read_only=True)
  user_type = serializers.CharField(source='user.user_type', read_only=True)

  class Meta:
    model = Todo
    fields = ['id', 'title', 'description', 'completed','user','user_name',
              'user_type','created_at','updated_at']
    read_only_fields = ['id','created_at','updated_at','user']


