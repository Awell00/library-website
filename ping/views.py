from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
import sqlite3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from .forms import InputForms
# from .forms import x
 
# Create your views here.


#@csrf_exempt

# def ajouter_adherent(adding):
#     nom=adding
#     cur = con.cursor()
#     con.commit()
#     prenom="prenom"
#     adresse="adresse"
#     tel="tel"
#     requete='INSERT INTO adherent(nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
#     cur.execute(requete)
    

# def ajouter_adherent():
#     nom=input("Nom: ")
#     prenom=input("Prénom du nouvel adhérent ?: ")
#     adresse=input("Adresse: ")
#     tel=input("Son tel: ")
#     requete='INSERT INTO adherent(nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
#     cur.execute(requete)
#     res3 = cur.execute("SELECT nomAdherent FROM adherent")
#     con.commit()
#     return res3.fetchall()

con2 = sqlite3.connect("bibliotheque.db")
cur2 = con2.cursor()
res = cur2.execute('SELECT * FROM adherent')
con2.commit()

# test = ajouter_adherent()

# test = res.fetchall()

name = res.fetchall()


def index(response):
    return render(response, 'ping/base.html', {"name": name})

def home(response):
    return render(response, 'ping/home.html', {})

def liste(response):
    return render(response, 'ping/liste.html', {"name": "test"})



@csrf_exempt
def add(request):
    liste1= []
    # con = sqlite3.connect("bibliotheque.db")
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = InputForms(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponseRedirect('')

    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = InputForms()
    data = request.POST
    nom_data = data.get("nom", "")
    prenom_data = data.get("prenom", "")
    adresse_data = data.get("adresse", "")
    tel_data = data.get("tel", "")
    # liste1.append(nom_data)
    # liste1.append(prenom_data)
    
    con = sqlite3.connect("bibliotheque.db")

    nom=nom_data
    prenom=prenom_data
    adresse=adresse_data
    tel=tel_data
    requete='INSERT OR REPLACE INTO adherent(nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
    cur = con.cursor()
    cur.execute(requete)
    res3 = cur.execute("SELECT * FROM adherent")
    con.commit()
    print(res3.fetchall())

    return render(request, 'ping/add.html')
    
