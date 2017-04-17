from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest


def home(request):
    return HttpResponse("Hello, world!")




def signup(request):
    return HttpResponse("Hello, world!")




def signup_success(request):
    return HttpResponse("Hello, world!")




def check_status(request):
    return HttpResponse("Hello, world!")




def edit(request):
    return HttpResponse("Hello, world!")




def update(request):
    return HttpResponse("Hello, world!")




def logout(request):
    return HttpResponse("Hello, world!")




def funnel(request):
    return HttpResponse("Hello, world!")




def errorpage(request):
    return HttpResponse("Hello, world!")




def bulk_upload(request, count):
    return HttpResponse("Hello, world!")


