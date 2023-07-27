"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from topic.forms import PasswordResettingForm

from topic.views import (
    topic_list_view,
    topic_detail_view,
    add_topic,
    add_skill,
    update_topic,
    delete_topic,
    skill_update,
    skill_edit,
    skill_delete,
    list_students,
    view_passwords,
    edit_class,
    edit_class_name,
    edit_student,
    delete_student,
    add_student,
    delete_class,
    student_topics,
    student_detail,
    by_student,
    by_student_pick_topic,
    by_student_view,
    by_student_update,
    by_subject,
    register,
    update_user,
    add_class,
    add_class_next,
    PasswordsChangeView,
    password_success,
    PasswordSettingView,
    PasswordResettingView,
)

from .views import (
    home_page,
    login_page,
    logout_page,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('register/', register),
    path('update_user/', update_user),
    path('password/', PasswordsChangeView.as_view(template_name='form.html')),
    path('password/success/', password_success, name='password_success'),
    path('login/', include("django.contrib.auth.urls")),
    path('your_classes/', list_students),
    path('your_classes/<int:pk>/passwords/', view_passwords),
    path('your_classes/<int:pk>/edit/', edit_class),
    path('your_classes/<int:pk>/edit/name/', edit_class_name),
    path('your_classes/<int:pk1>/edit/<int:pk2>/', edit_student),
    path('your_classes/<int:pk1>/edit/<int:pk2>/delete/', delete_student),
    path('your_classes/<int:pk>/edit/add/', add_student),
    path('your_classes/<int:pk>/edit/delete/', delete_class),
    path('your_classes/add/', add_class),
    path('your_classes/add/next/<int:pk>/', add_class_next),
    path('login/', login_page),
    path('logout/', logout_page),
    path('add/', add_topic),
    path('topic/', by_subject),
    path('topic/<str:slug>/', topic_detail_view),  
    path('topic/<str:slug1>/skill/<str:slug2>', skill_update),  
    path('topic/<str:slug1>/skill/<str:slug2>/edit/', skill_edit),  
    path('topic/<str:slug1>/skill/<str:slug2>/delete/', skill_delete),  
    path('topic/<str:slug>/add/', add_skill),
    path('topic/<str:slug>/edit/', update_topic),
    path('topic/<str:slug>/delete/', delete_topic),
    path('student/topics/', student_topics),
    path('student/topics/<str:slug>', student_detail),
    path('by_student/', by_student),
    path('by_student/<int:pk>/', by_student_pick_topic),
    path('by_student/<int:pk>/topic/<str:slug>/', by_student_view),    
    path('by_student/<int:pk>/topic/<str:slug>/update/', by_student_update),

    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html", form_class=PasswordResettingForm), 
         name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
         PasswordSettingView.as_view(template_name="password_reset_form.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
         name="password_reset_complete")
]

urlpatterns += staticfiles_urlpatterns()
