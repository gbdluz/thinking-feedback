from django.urls import path

from .views import student_detail, student_topics

urlpatterns = [
    path("topics/", student_topics),
    path("topics/<int:pk>/", student_detail),
]
