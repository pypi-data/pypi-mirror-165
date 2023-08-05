from django.shortcuts import render, redirect, get_object_or_404

from . import registration_token
from .models import Captcha


def generate(request):
    return redirect("syngo:check", pk=Captcha.generate().pk)


def check(request, pk):
    captcha = get_object_or_404(Captcha, pk=pk)
    if request.POST:
        if request.POST.get("guess", "").lower() == captcha.secret.lower():
            captcha.delete()
            token = registration_token().json()["token"]
            return render(request, "syngo/success.html", {"token": token})
    return render(request, "syngo/check.html", {"captcha": captcha})
