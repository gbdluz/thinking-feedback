from django.urls import path

from task.views import add_task, update_task, delete_task, add_task_generator, update_task_generator, \
    delete_task_generator

urlpatterns = [
    path("<int:pk_topic>/skill_level/<int:pk_skill_level>/task/add/", add_task),
    path("<int:pk_topic>/task/<int:pk_task>/edit/", update_task),
    path("<int:pk_topic>/task/<int:pk_task>/delete/", delete_task),
    path("<int:pk_topic>/skill_level/<int:pk_skill_level>/generator/add/", add_task_generator),
    path("<int:pk_topic>/generator/<int:pk_generator>/edit/", update_task_generator),
    path("<int:pk_topic>/generator/<int:pk_generator>/delete/", delete_task_generator),
]
