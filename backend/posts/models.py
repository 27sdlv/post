from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=75)
    body=models.TextField()
    slug=models.SlugField()
    date=models.DateTimeField(auto_now_add=True)
    banner=models.ImageField(default='fallback.jpg', blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,default=None, null=True,related_name='authored_posts')
    likes=models.ManyToManyField(User, default=None, blank=True,related_name='liked_posts')
    dislikes=models.ManyToManyField(User, default=None, blank=True,related_name='disliked_posts')
    views=models.IntegerField(default=0)    

    def __str__(self):
        return self.title
class Comment(models.Model):
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,default=None, null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,default=None, null=True)
    
    def __str__(self):
        return self.body

   