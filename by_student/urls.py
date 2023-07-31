from django.urls import path, include

from .views import (
    by_student,
    by_student_pick_topic,
    by_student_view,
    by_student_update,
    by_student_edit,
)

urlpatterns = [
    path('', by_student),
    path('<int:pk>/', by_student_pick_topic),
    path('<int:pk>/topic/<str:slug>/', by_student_view),    
    path('<int:pk>/topic/<str:slug>/update/', by_student_update),
    path('<int:pk>/topic/<str:slug>/edit/', by_student_edit),
]