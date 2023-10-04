from django.urls import path

from topic.views import (
    add_skill, add_topic, stage_all_topics, delete_topic,
    topic_edit_whole_topic_view, topic_student_view, change_skill_order,
    update_topic, add_skill_level, add_skill_to_skill_level, delete_skill, update_skill, delete_skill_level,
    update_skill_level,
)

urlpatterns = [
    path("", stage_all_topics),
    path("add/stage/<int:pk_stage>/", add_topic),
    path("<int:pk>/", topic_edit_whole_topic_view),
    path("<int:pk>/view/", topic_student_view),
    path("<int:pk1>/skill/<int:pk2>/edit/", update_skill),
    path("<int:pk1>/skill/<int:pk2>/delete/", delete_skill),
    path("<int:pk1>/skill/<int:pk2>/add_skill_level/", add_skill_level),
    path(
        "<int:pk1>/skill_level/<int:pk3>/add_skill_to_skill_level/",
        add_skill_to_skill_level,
    ),
    path(
        "<int:pk>/skill/<int:pk_skill>/change_order/<str:up_down>/",
        change_skill_order,
    ),
    path("<int:pk1>/skill_level/<int:pk3>/edit/", update_skill_level),
    path("<int:pk1>/skill_level/<int:pk3>/delete/", delete_skill_level),
    path("<int:pk>/add/", add_skill),
    path("<int:pk>/edit/", update_topic),
    path("<int:pk>/delete/", delete_topic),
]
