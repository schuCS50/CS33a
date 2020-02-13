from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def test(request):
    return HttpResponse("<h1>Test</h1>")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })

def render_test(request):
    return render(request, "hello/index.html")
