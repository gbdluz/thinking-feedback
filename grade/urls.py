from django.urls import path

from grade.views import grade_add, skill_grade_edit, skill_grade_edit_next, skill_grade_delete, skill_grade_delete_next

urlpatterns = [
    path("<int:pk1>/skill/<int:pk2>/", grade_add),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/", skill_grade_edit),
    path("<int:pk1>/skill/<int:pk2>/grade_edit/<int:level>/", skill_grade_edit_next),
    path("<int:pk1>/skill/<int:pk2>/grade_delete/", skill_grade_delete),
    path(
        "<int:pk1>/skill/<int:pk2>/grade_delete/<int:level>/", skill_grade_delete_next,
    ),
]
