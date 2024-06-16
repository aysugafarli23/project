# myapp/views.py
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
)
from .serializers import ModuleSerializer, ContentSerializer, ScoreSerializer
from ..models import Module, Content, Score
from rest_framework.filters import SearchFilter, OrderingFilter

class ModuleCreateAPIView(CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def perform_create(self, serializer):
        serializer.save()

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
        serializer.save()

class ContentCreateAPIView(CreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

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
