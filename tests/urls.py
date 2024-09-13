from django.urls import path
from .views import LevelTestView, EvaluateTestView

urlpatterns = [
    path('test/<str:level>/', LevelTestView.as_view(), name='get_test'),
    path('test/evaluate/', EvaluateTestView.as_view(), name='evaluate_test'),
]
