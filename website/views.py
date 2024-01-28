from django.shortcuts import render


def login(request):
    return render(request, 'loginpage.html')


def home(request):
    return render(request, 'home.html')
