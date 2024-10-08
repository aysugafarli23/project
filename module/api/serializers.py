from rest_framework import serializers
from ..models import Content, Section, Module, Lesson

class ContentSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Content
        fields = ['id', 'content_section', 'content_title', 'body', 'content_image', 'video_link']

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ['id', 'section_title', 'section_lesson']

class LessonSerializer(serializers.ModelSerializer):
    lesson_sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'lesson_module', 'lesson_title', 'lesson_image', 'lesson_sections']
        
class ModuleSerializer(serializers.ModelSerializer):
    module_lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'module_title','module_image', 'module_lessons']
        