# 認証関連の処理
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    """ログイン処理"""
    if request.user.is_authenticated:
        return redirect("category_selection")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("category_selection")
        else:
            messages.error(request, "ユーザーIDまたはパスワードが間違っています")
    
    return render(request, "mathquiz/login.html")

def register_view(request):
    """新規ユーザー登録"""
    if request.user.is_authenticated:
        return redirect("category_selection")
    
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "このユーザーIDは既に使用されています")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect("category_selection")
    
    return render(request, "mathquiz/register.html")

def logout_view(request):
    """ログアウト処理"""
    logout(request)
    return redirect("login")
