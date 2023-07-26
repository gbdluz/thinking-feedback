from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from topic.models import Topic

qs = Topic.objects.all()


def home_page(request):
    return render(request, 'title.html', {'title': 'Welcome to ThinkingFeedback!'})
        


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        
        template_name = "login.html"
        context = {'topic_list': qs}
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.success(request, message="There was an error logging in. Try again")
                return redirect("/login")
        else:
            return render(request, template_name, context)
    
def logout_page(request):
    logout(request)
    messages.success(request, message="You were logged out")
    return redirect('/')





