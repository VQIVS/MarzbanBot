from django.shortcuts import render


def send_message(request):
    return render(request, 'message.html')
