from django.urls import path, include

from .views import (
    student_topics,
    student_detail,
)

urlpatterns = [
    path('topics/', student_topics),
    path('topics/<str:slug>', student_detail),
]