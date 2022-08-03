from rest_framework import serializers
from djangoTask.models import todo

class todoSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    due_date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z')
    class Meta:
        model = todo
        fields = [
        'id',
        'title',
        'description',
        'creation_date',
        'due_date',
        'status',
        'tags', ]
