from django.shortcuts import render
from django.http import HttpResponse
import sqlite3


# def ajouter_adherent():
#     nom=input("Nom du nouvel adhérent ?: ")
#     prenom=input("Prénom du nouvel adhérent ?: ")
#     adresse=input("Adresse: ")
#     tel=input("Son tel: ")
#     requete='INSERT INTO adherent(nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
#     cur.execute(requete)
    

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
# res = cur.execute('SELECT * FROM Test')
con.commit()
test = ajouter_adherent()

# test = res.fetchall()



def index(response):
    return render(response, 'ping/base.html', {"name": test})

def home(response):
    return render(response, 'ping/home.html', {})

def liste(response):
    return render(response, 'ping/liste.html', {"name": test})

def add(response):
    return render(response, 'ping/add.html', {})