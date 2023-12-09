from django.urls import path

from grade import views
from grade.views import add_grade, delete_grade, skill_grade_edit, skill_grade_edit_next, skill_grade_delete, skill_grade_delete_next, \
    choose_topic_students, choose_test, choose_stage, choose_student_test

urlpatterns = [
    path("", choose_stage),
    path("stage/<int:pk>/topic/", choose_topic_students),
    path("stage/<int:pk>/test/", choose_test),
    path("stage/<int:pk>/student_test/", choose_student_test),
    path("add/", add_grade),
    path("delete/", delete_grade),
    # TODO: remove all below
    path('create/', views.GradeCreateView.as_view(), name='create_grade'),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/", skill_grade_edit),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/<int:level>/", skill_grade_edit_next),
    path("<int:pk1>/skill/<int:pk2>/grade_delete/", skill_grade_delete),
    path(
        "<int:pk1>/skill/<int:pk2>/grade_delete/<int:level>/", skill_grade_delete_next,
    ),
]
