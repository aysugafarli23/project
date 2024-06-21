from django.urls import path
from .views import *

app_name = "module"

urlpatterns = [    
    path("units/create/", UnitCreateAPIView.as_view(), name="unit-create"),
    path("units/list/", UnitListAPIView.as_view(), name="unit-list"),
    path("units/detail/<pk>/", UnitDetailAPIView.as_view(), name="unit-detail"),
    path("units/update/<pk>/", UnitUpdateAPIView.as_view(), name="unit-update"),
    path("units/delete/<pk>/", UnitDeleteAPIView.as_view(), name="unit-delete"),
    
    path("modules/create/", ModuleCreateAPIView.as_view(), name="module-create"),
    path("modules/list/", ModuleListAPIView.as_view(), name="module-list"),
    path("modules/detail/<pk>/", ModuleDetailAPIView.as_view(), name="module-detail"),
    path("modules/update/<pk>/", ModuleUpdateAPIView.as_view(), name="module-update"),
    path("modules/delete/<pk>/", ModuleDeleteAPIView.as_view(), name="module-delete"),
    
    path("sections/create/", SectionCreateAPIView.as_view(), name="section-create"),
    path("sections/list/", SectionListAPIView.as_view(), name="section-list"),
    path("sections/detail/<pk>/", SectionDetailAPIView.as_view(), name="section-detail"),
    path("sections/update/<pk>/", SectionUpdateAPIView.as_view(), name="section-update"),
    path("sections/delete/<pk>/", SectionDeleteAPIView.as_view(), name="section-delete"),
    
    path("contents/create/", ContentCreateAPIView.as_view(), name="content-create"),
    path("contents/list/", ContentListAPIView.as_view(), name="content-list"),
    path("contents/detail/<pk>/", ContentDetailAPIView.as_view(), name="content-detail"),
    path("contents/update/<pk>/", ContentUpdateAPIView.as_view(), name="content-update"),
    path("contents/delete/<pk>/", ContentDeleteAPIView.as_view(), name="content-delete"),

    path("scores/create/", ScoreCreateAPIView.as_view(), name="score-create"),
    path("scores/list/", ScoreListAPIView.as_view(), name="score-list"),
    path("scores/detail/<pk>/", ScoreDetailAPIView.as_view(), name="score-detail"),
    path("scores/update/<pk>/", ScoreUpdateAPIView.as_view(), name="score-update"),
    path("scores/delete/<pk>/", ScoreDeleteAPIView.as_view(), name="score-delete"),
]