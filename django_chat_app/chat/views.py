from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(
    login_url="/login/"
)  # Leitet automatisch auf die Login Seite weiter wenn nicht eingeloggt.
def index(request):
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )
    chatMessages = Message.objects.filter(chat__id=1)
    return render(
        request, "chat/index.html", {"username": "Martin", "messages": chatMessages}
    )


def login_view(request):
    redirect = request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(
                request.POST.get("redirect")
            )  # Führt dazu, dass der User wieder auf die Seite gelangt, auf die er vor dem Login war
        else:
            return render(
                request,
                "auth/login.html",
                {"wrongPassword": True, "redirect": redirect},
            )
    return render(request, "auth/login.html", {"redirect": redirect})


def register_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"],
        )
        return HttpResponseRedirect("/login/")
    return render(request, "auth/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")
