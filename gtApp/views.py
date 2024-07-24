from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
import requests as rs
# Create your views here.


def index(request):
    return render(request, "index.html")


def userReg(request):
    msg = ''
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            msg = "Username already exists"
        else:
            user = User.objects.create_user(
                username=email, password=password)
            user.save()
            customer = Users.objects.create(
                name=name, email=email, phone=phone, address=address, user=user)
            customer.save()
            msg = "Registration successful"

    return render(request, "userReg.html", {"msg": msg})

def login(request):
    msg = ""
    if (request.POST):
        email = request.POST.get("uName")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminHome")
            else:
                data = Users.objects.get(email=email)
                request.session['uid'] = data.id
                return redirect('/userHome')
        else:
            msg = "Invalid Credentials"

    return render(request, "login.html", {"msg": msg})


def adminHome(request):
    return render(request, "adminHome.html")

def adminUsers(request):
    data = Users.objects.all()
    return render(request, "adminUsers.html",{"data":data})

def adminApproveUser(request):
    id = request.GET['id']
    status = request.GET['status']
    usr = User.objects.get(id=id)
    usr.is_active = status
    usr.save()
    return redirect("/adminUsers")

def adminBlogs(request):
    data = Blogs.objects.all()
    if "search" in request.POST:
        search = request.POST['search']
        data = Blogs.objects.filter(Q(title__contains=search) | Q(desc__contains=search)).order_by("-id")
    return render(request, "adminBlogs.html",{"data":data})

def adminViewBlogs(request):
    id = request.GET['id']
    data = Blogs.objects.get(id=id)
    comments = Comments.objects.filter(blogs=id)
    return render(request, "adminViewBlogs.html",{"data":data,"comments":comments})

def adminDeleteBlog(request):
    id = request.GET['id']
    usr = Blogs.objects.get(id=id)
    usr.delete()
    return redirect("/adminBlogs")

def userHome(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    return render(request, "userHome.html", {"user": user})

def userGames(request):
    data = ''
    response = rs.get(f'https://api.rawg.io/api/games?key=8f1d0ab12e4f4172a467f41a213c5707')
    if response.status_code == 200:
        data = response.json()  
        data = data['results']
        print(data)
    if request.POST:
        search = request.POST['search']
        response = rs.get(f'https://api.rawg.io/api/games?key=8f1d0ab12e4f4172a467f41a213c5707&search={search}')
        if response.status_code == 200:
            data = response.json()  
            data = data['results']
    return render(request, "userGames.html", {"data": data})

def userViewGame(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    id = request.GET['id']
    data = ''
    response = rs.get(f'https://api.rawg.io/api/games/{id}?key=8f1d0ab12e4f4172a467f41a213c5707')
    if response.status_code == 200:
        data = response.json()  
    if request.POST:
        status = request.POST['status']
        name = data['name']
        img = data['background_image']
        print(status,name)
        r = Progress.objects.create(gameid=id,status=status,name=name,users=user,img=img)
        r.save()
        return redirect("/userProgress")
    return render(request, "userViewGame.html", {"data": data})

def userProgress(request):
    uid = request.session['uid']
    data = Progress.objects.filter(users=uid).order_by("-id")
    print(data)
    return render(request, "userProgress.html", {"data": data})

def userDeletProgress(request):
    id = request.GET['id']
    data = Progress.objects.get(id=id)
    data.delete()

    return redirect("/userProgress")

def userBlogs(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    data = Blogs.objects.exclude(users=user).order_by("-id")
    if 'title' in request.POST:
        title = request.POST['title']
        desc = request.POST['desc']
        img = request.FILES['img']
        ins = Blogs.objects.create(users=user,title=title,desc=desc,img=img)
        ins.save()
    if "search" in request.POST:
        search = request.POST['search']
        data = Blogs.objects.filter(Q(title__contains=search) | Q(desc__contains=search)).exclude(users=user).order_by("-id")
    return render(request,"userBlogs.html", {"data":data})

def userViewBlogs(request):
    uid = request.session['uid']
    id = request.GET['id']
    user = Users.objects.get(id=uid)
    data = Blogs.objects.get(id=id)
    if request.POST:
        comment = request.POST['comment']
        db = Comments.objects.create(comment=comment, blogs=data, users=user)
        db.save()
    comments = Comments.objects.filter(blogs=id)
    return render(request,"userViewBlogs.html", {"data":data, "comments":comments})

def userViewUsers(request):
    id = request.GET['id']
    user = Users.objects.get(id=id)
    data = Progress.objects.filter(users=user).order_by("-id")
    return render(request,"userViewUsers.html", {"user":user, "data":data})

def userVideos(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    if request.POST:
        video = request.FILES['video']
        desc = request.POST['desc']
        db = Videos.objects.create(video=video, desc=desc, users=user)
        db.save()
    data = Videos.objects.filter(users=uid).order_by("-id")
    return render(request,"userVideos.html", {"data":data})

def userDeleteVideo(request):
    id = request.GET['id']
    vid = Videos.objects.get(id=id)
    vid.delete()
    return redirect("/userVideos")

def userViewVideos(request):
    uid = request.session['uid']
    user = Users.objects.get(id=uid)
    data = Videos.objects.exclude(users=user).order_by("-id")
    if request.POST:
        search = request.POST['search']
        data = Videos.objects.filter(desc__contains=search).order_by("-id")
    return render(request, "userViewVideos.html", {"data": data})

def adminDeleteUser(request):
    id = request.GET['id']
    usr = User.objects.get(id=id)
    usr.delete()
    return redirect("/adminUsers")
