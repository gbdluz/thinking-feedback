from django.urls import path, include

from .views import (
    student_topics,
    student_detail,
)

urlpatterns = [
    path('topics/', student_topics),
    path('topics/<int:pk>/', student_detail),
]