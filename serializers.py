from rest_framework import serializers
from djangoTask.models import todo
from django.contrib.auth.models import User

class todoSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    due_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    owner=serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = todo
        fields = [
        'id',
        'title',
        'description',
        'creation_date',
        'due_date',
        'status',
        'tags',
        'owner', ]

class UserSerializer(serializers.ModelSerializer):
    todos = serializers.PrimaryKeyRelatedField(many=True,queryset=todo.objects.all())
    class Meta:
        model=User
        fields=['id','username','todos']
