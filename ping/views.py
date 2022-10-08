from django.http import HttpResponse

def index(response):
    return HttpResponse("Hello world!")

def v1(response):
    return HttpResponse("V1")
