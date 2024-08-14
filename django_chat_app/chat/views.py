from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.middleware.csrf import CsrfViewMiddleware


@login_required(
    login_url="/login/"
)  # Leitet automatisch auf die Login Seite weiter wenn nicht eingeloggt
def index(request):
    """
    Comment for the function.
    """
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        receiver, create = User.objects.get_or_create(username="zuegelwagen")
        myChat, create = Chat.objects.get_or_create(id=1)
        new_message = (
            Message.objects.create(  # Erstellt einen neuen Eintrag in der Datenbank
                text=request.POST["textmessage"],
                chat=myChat,
                author=request.user,
                receiver=receiver,
            )
        )
        serialized_obj = serializers.serialize(
            "json", [new_message]
        )  # Erstellt aus der Antwort ein Object
        return JsonResponse(
            serialized_obj[1:-1], safe=False
        )  # safe=False braucht es, sonst verlangt er gewisse Felder. [1:-1] braucht es, da ein Array zurückgegeben wird. Mit dem Zusatz wird ein JSON zurückgegeben
    chatMessages = Message.objects.filter(chat__id=1)
    return render(
        request, "chat/index.html", {"messages": chatMessages}
    )


def login_view(request):
    redirect = request.GET.get("next", "/chat/")
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
