from rest_framework import serializers
from ..models import Content, Section, Module, Lesson, Score

class ContentSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Content
        fields = ['id', 'content__lesson', 'content__section', 'content__title', 'body', 'content__image', 'audio', 'audio_file', 'video_link']

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ['id', 'section_title', 'section_lesson']

class LessonSerializer(serializers.ModelSerializer):
    lesson__sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'lesson_module', 'lesson_title', 'lesson_sections']
        
class ModuleSerializer(serializers.ModelSerializer):
    module__lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'module_title','module_image', 'module_lessons']
        
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['section_title', 'section_lesson']
