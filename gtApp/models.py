from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Progress(models.Model):
    date = models.DateField(auto_now_add=True)
    gameid = models.CharField(max_length=20)
    name = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=200)
    img=models.URLField(null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)

class Blogs(models.Model):
    date = models.DateField(auto_now=True,null=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=20)
    desc=models.CharField(max_length=200)
    img=models.FileField()

class Videos(models.Model):
    date = models.DateField(auto_now_add=True)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos')
    desc = models.CharField(max_length=200)

class Comments(models.Model):
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)