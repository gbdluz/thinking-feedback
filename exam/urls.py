from django.urls import path

from .views import (
    choose_stage, create_test, manage_test, create_student_test, manage_student_test, generate_test, generate_student_test,
)

urlpatterns = [
    path("", choose_stage),
    path("add/", create_test),
    path("<int:pk>/manage/", manage_test),
    path("<int:pk>/generate/", generate_test),
    path("add/student/", create_student_test),
    path("student/<int:pk>/manage/", manage_student_test),
    path("student/<int:pk>/generate/", generate_student_test),
]
