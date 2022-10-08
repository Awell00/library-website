from django.http import HttpResponse
from .models import ToDOLIst, Item

def index(response, id):
    ls = ToDOLIst.objects.get(id=id)
    return HttpResponse("<h1>%s</h1>" % ls.name)

