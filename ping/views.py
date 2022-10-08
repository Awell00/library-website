from django.http import HttpResponse
from .models import ToDOLIst, Item

def index(response, name):
    ls = ToDOLIst.objects.get(name=name)
    item = ls.item_set.get(id=1)
    return HttpResponse("<h1>%s</h1>" % (ls.name, item.name))

