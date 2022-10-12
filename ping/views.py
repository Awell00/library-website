from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import isbnlib 
import uuid

# words = "Harry Potter Chamber of Secrets"
# isbn = "9782070585205"

# book = isbnlib.meta(isbn)
# word2 = isbnlib.goom(words)
# cover = isbnlib.cover(isbn)

# print(book["Authors"])
# print(book["Title"])

# print(word2)
# print(cover)






def index(response):
    con2 = sqlite3.connect("bibliotheque.db")
    cur2 = con2.cursor()
    res = cur2.execute('SELECT * FROM adherent')
    con2.commit()

    name = res.fetchall()
    return render(response, 'ping/base.html', {"name": name})

def home(response):
    return render(response, 'ping/home.html', {})

def liste(response):
    return render(response, 'ping/liste.html', {"name": "test"})

@csrf_exempt
def add(request):
    liste=[]
    id = str(uuid.uuid4())[:8]
    data = request.POST
    nom_data = data.get("nom", "")
    prenom_data = data.get("prenom", "")
    adresse_data = data.get("adresse", "")
    tel_data = data.get("tel", "")

    con = sqlite3.connect("bibliotheque.db")

    nom=nom_data
    prenom=prenom_data
    adresse=adresse_data
    tel=tel_data
    if nom_data == '' or prenom_data == "" or adresse_data == "" or tel_data == "":
        pass
    else:
        res ='INSERT OR REPLACE INTO adherent(identifiant, nomAdherent, prenomAdherent, adresse, telephone) VALUES ("'+id+'","'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'")'
        cur = con.cursor()
        cur.execute(res)
        
        con.commit()
    # for item in res2.fetchall():
    #     liste.append(item)
    cur = con.cursor()
    res2 = cur.execute("SELECT * FROM adherent")
    con.commit()

    for item in res2.fetchall():
        liste.append(item[1])

    print(liste)

    return render(request, 'ping/add.html', {"adherent": liste})

@csrf_exempt
def delete(request):
    liste2 = []
    data2 = request.POST
    id_data = data2.get("id", "")

    identifiant=id_data
    print(identifiant)
    requete="delete from adherent where identifiant =:identifiant"
    
    con3 = sqlite3.connect("bibliotheque.db")

    cur = con3.cursor()
    res2 = "SELECT * FROM adherent where identifiant =:identifiant"
    test5 = cur.execute(res2,{"identifiant":identifiant})
    liste2.append(test5.fetchall())
    cur.execute(requete,{"identifiant":identifiant})
    
    delete = liste2
    con3.commit()

    return render(request, 'ping/delete.html', {"element_delete": delete})
    
