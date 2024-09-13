from django.urls import path
from .views import LevelTestView, EvaluateLevelTestView

urlpatterns = [
    path('evaluate/<str:level>/', EvaluateLevelTestView.as_view(), name='evaluate_test_level'),
    path('<str:level>/', LevelTestView.as_view(), name='get_test'),
]
