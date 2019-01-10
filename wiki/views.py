# from django.http import HttpResponse
from django.shortcuts import render

def wiki_home(request):
    return render(request, "wiki_home.html", {})
