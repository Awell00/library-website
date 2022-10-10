from readline import add_history
from django.http import HttpResponse
from .models import ToDOLIst, Item
import sqlite3


def ajouter_adherent():
    nom=input("Nom du nouvel adhérent ?: ")
    prenom=input("Prénom du nouvel adhérent ?: ")
    adresse=input("Adresse: ")
    tel=input("Son tel: ")
    requete='INSERT INTO adherent(nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
    cur.execute(requete)
    res3 = cur.execute("SELECT nomAdherent FROM adherent")
    con.commit()
    return res3.fetchall()

con = sqlite3.connect("bibliotheque.db")
cur = con.cursor()
res = cur.execute('SELECT * FROM Test')
con.commit()
test = ajouter_adherent()

# test = res.fetchall()



def index(response, name):
    # ls = ToDOLIst.objects.get(name=name)
    # item = ls.item_set.get(id=1)
    return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" % (test, name))

