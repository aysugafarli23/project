# myapp/serializers.py
from rest_framework import serializers
from ..models import Unit, Module, Content, Section, Score

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())  # Add this line

    class Meta:
        model = Section
        fields = ['id', 'title', 'contents', 'module']

class ModuleSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'unit', 'image', 'title', 'description', 'sections']
        
class UnitSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'title', 'modules']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'user', 'content', 'score']
