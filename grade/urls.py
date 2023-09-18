from django.urls import path

from grade import views
from grade.views import add_grade, skill_grade_edit, skill_grade_edit_next, skill_grade_delete, skill_grade_delete_next, \
    choose_stage_topic_students

urlpatterns = [
    path("", choose_stage_topic_students),
    # TODO: use one of below
    path("add/", add_grade),
    path('create/', views.GradeCreateView.as_view(), name='create_grade'),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/", skill_grade_edit),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/<int:level>/", skill_grade_edit_next),
    path("<int:pk1>/skill/<int:pk2>/grade_delete/", skill_grade_delete),
    path(
        "<int:pk1>/skill/<int:pk2>/grade_delete/<int:level>/", skill_grade_delete_next,
    ),
]
