from django.http import HttpResponse
from .models import ToDOLIst, Item
import sqlite3  


def ajouter_adherent():
    nom=input("Nom du nouvel adhérent ?: ")
    # prenom=input("Prénom du nouvel adhérent ?: ")
    # adresse=input("Adresse: ")
    # tel=input("Son tel: ")
    res = cur.execute('INSERT INTO '+nom+' VALUES("test","test","test")')
    con.commit()
    test = cur.execute('SELECT * FROM '+nom)
    test2 = test.fetchall()
    return test2

con = sqlite3.connect("bibliotheque.db")
cur = con.cursor()
res = cur.execute('SELECT * FROM h')
con.commit()
test = ajouter_adherent()

def index(response, name):
    
    ls = ToDOLIst.objects.get(name=name)
    item = ls.item_set.get(id=1)
    return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" % (test, item.text))

print(ajouter_adherent())