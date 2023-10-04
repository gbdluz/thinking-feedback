from django.urls import path

from .views import (
    by_student, by_student_edit, by_student_pick_topic,
    by_student_update, by_student_view,
)

urlpatterns = [
    path("", by_student),
    path("<int:pk>/", by_student_pick_topic),
    path("<int:pk1>/topic/<int:pk2>/", by_student_view),
    path("<int:pk1>/topic/<int:pk2>/update/", by_student_update),
    path("<int:pk1>/topic/<int:pk2>/edit/", by_student_edit),
]
