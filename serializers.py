from rest_framework import serializers
from djangoTask.models import todo

class todoSerializer(serializers.ModelSerializer):
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
