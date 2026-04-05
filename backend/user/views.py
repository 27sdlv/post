from django.shortcuts import render, redirect                                                                
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.models import User 
from posts.models import Post   


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            auth_login(request,form.save())
            return redirect('posts:list') # Redirects to post page
    else:
        form = UserCreationForm()

        
    return render(request, 'user/register.html', {'form': form})  

def login(request):
    if request.method=="POST":
        form =AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('posts:list')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def logout(request):
    if request.method=="POST":
        auth_logout(request)
        return redirect('posts:list')

def profile(request,username):
    user=User.objects.get(username=username)
    posts=Post.objects.filter(author=user)
    return render(request,'user/profile.html',{'user':user,'posts':posts})