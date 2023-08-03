from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from .views import (
    topic_detail_view,
    add_topic,
    add_skill,
    update_topic,
    delete_topic,
    skill_update,
    skill_edit,
    skill_delete,
    skill_grade_edit,
    skill_grade_edit_next,
    skill_grade_delete,
    skill_grade_delete_next,
    by_subject,
)

urlpatterns = [
    path('', by_subject),
    path('add/', add_topic),
    path('<int:pk>/', topic_detail_view),  
    path('<int:pk1>/skill/<int:pk2>/', skill_update),  
    path('<int:pk1>/skill/<int:pk2>/edit/', skill_edit),  
    path('<int:pk1>/skill/<int:pk2>/delete/', skill_delete),  
    path('<int:pk1>/skill/<int:pk2>/grade_edit/', skill_grade_edit),  
    path('<int:pk1>/skill/<int:pk2>/grade_edit/<int:level>/', skill_grade_edit_next),  
    path('<int:pk1>/skill/<int:pk2>/grade_delete/', skill_grade_delete),  
    path('<int:pk1>/skill/<int:pk2>/grade_delete/<int:level>/', skill_grade_delete_next), 
    path('<int:pk>/add/', add_skill),
    path('<int:pk>/edit/', update_topic),
    path('<int:pk>/delete/', delete_topic),
]