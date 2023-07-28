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
    by_subject,
)

urlpatterns = [
    path('', by_subject),
    path('add/', add_topic),
    path('<str:slug>/', topic_detail_view),  
    path('<str:slug1>/skill/<str:slug2>', skill_update),  
    path('<str:slug1>/skill/<str:slug2>/edit/', skill_edit),  
    path('<str:slug1>/skill/<str:slug2>/delete/', skill_delete),  
    path('<str:slug>/add/', add_skill),
    path('<str:slug>/edit/', update_topic),
    path('<str:slug>/delete/', delete_topic),
]