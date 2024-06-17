# myapp/views.py
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
)
from .serializers import UnitSerializer, ModuleSerializer, SectionSerializer, ContentSerializer, ScoreSerializer
from ..models import Unit, Module, Section, Content, Score
from rest_framework.filters import SearchFilter, OrderingFilter


class UnitCreateAPIView(CreateAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class UnitListAPIView(ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
        
class UnitDetailAPIView(RetrieveAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    lookup_field = 'pk'
    
class UnitDeleteAPIView(DestroyAPIView):
    queryset =Unit.objects.all()
    serializer_class =UnitSerializer
    lookup_field = "pk"
    
class UnitUpdateAPIView(UpdateAPIView):
    queryset =Unit.objects.all()
    serializer_class =UnitSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
       serializer.save(user = self.request.user)
       

class ModuleCreateAPIView(CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)

class ModuleListAPIView(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ["id", "unit"]
    search_fields = ["title", "description"]

class ModuleDetailAPIView(RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "pk"

class ModuleDeleteAPIView(DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = "pk"

class ModuleUpdateAPIView(UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
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


class ScoreCreateAPIView(CreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScoreListAPIView(ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ScoreDetailAPIView(RetrieveAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = "pk"

class ScoreDeleteAPIView(DestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = "pk"

class ScoreUpdateAPIView(UpdateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = "pk"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
