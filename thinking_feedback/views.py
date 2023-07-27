from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from topic.models import Topic

qs = Topic.objects.all()



        








