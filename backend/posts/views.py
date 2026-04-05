from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    
    # Track view using session (works for anon and logged-in, persistent, once per post)
    viewed_posts = request.session.get('viewed_posts', [])
    if post.id not in viewed_posts:
        post.views += 1
        post.save()
        viewed_posts.append(post.id)
        request.session['viewed_posts'] = viewed_posts

    if request.method=='POST':
        form=forms.CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            return redirect('posts:page',slug=post.slug)
    else:
        form=forms.CommentForm()
    return render(request, 'posts/post_page.html', {'post': post,'form':form})
@login_required(login_url='/user/login/')
def new_post(request):
    form=forms.CreatePostForm()
    if request.method == 'POST':
        form=forms.CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list')
    else:
        form=forms.CreatePostForm() 
    return render(request,'posts/new_post.html',{'form':form})
@login_required(login_url='/user/login/')
def edit_post(request,slug):
    post=Post.objects.get(slug=slug)
    if request.user !=post.author:
        return redirect('posts:list')
    
    if request.method=='POST':
            form=forms.CreatePostForm(request.POST,request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:page',slug=post.slug)
    else:
        form=forms.CreatePostForm(instance=post)
    return render(request,'posts/edit_post.html',{'form':form,'post':post})

@login_required(login_url='/user/login')
def delete_post(request,slug):
    post=Post.objects.get(slug=slug)
    if request.user !=post.author:
        return redirect('posts:list')
    
    if request.method=='POST':
        post.delete()
        return redirect('posts:list')
    return render(request,'posts/delete_post.html',{'post':post})
@login_required(login_url='/user/login')
def like_post(request,slug):
    post=Post.objects.get(slug=slug)
    if request.method=='POST':
        action = request.POST.get('action')
        
        if action == 'like':
            # Remove dislike if exists
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)
            # Add like if not exists
            if not post.likes.filter(id=request.user.id).exists():
                post.likes.add(request.user)
                
        elif action == 'unlike':
            # Remove like if exists
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            # Add dislike if not exists
            if not post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.add(request.user)
                
    return redirect('posts:page',slug=post.slug)
