# myapp/views.py
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
)
from .serializers import ModuleSerializer, LessonSerializer, SectionSerializer, ContentSerializer
from ..models import Module, Lesson, Section, Content
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ModuleCreateAPIView(CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
        
class ModuleDetailAPIView(RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'pk'
    
class ModuleDeleteAPIView(DestroyAPIView):
    queryset =Module.objects.all()
    serializer_class =ModuleSerializer
    lookup_field = "pk"
    
class ModuleUpdateAPIView(UpdateAPIView):
    queryset =Module.objects.all()
    serializer_class =ModuleSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
       serializer.save(user = self.request.user)
       

class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['lesson_module']
    search_fields = ['module_title', 'lesson_title']

class LessonDetailAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "pk"

class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "pk"

class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)
        
        
class SectionCreateAPIView(CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class SectionListAPIView(ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
        
class SectionDetailAPIView(RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'pk'
    
class SectionDeleteAPIView(DestroyAPIView):
    queryset =Section.objects.all()
    serializer_class =SectionSerializer
    lookup_field = "pk"
    
class SectionUpdateAPIView(UpdateAPIView):
    queryset =Section.objects.all()
    serializer_class =SectionSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
       serializer.save(user = self.request.user)
    
    
class ContentCreateAPIView(CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class ContentListAPIView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class ContentDetailAPIView(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "pk"

class ContentDeleteAPIView(DestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "pk"

class ContentUpdateAPIView(UpdateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

