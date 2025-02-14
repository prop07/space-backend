from rest_framework import serializers
from app.models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'details',  'lastUpdate', 'addedTime']