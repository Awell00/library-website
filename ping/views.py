from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import isbnlib 
import uuid


def index(response):
    con2 = sqlite3.connect("bibliotheque.db")
    cur2 = con2.cursor()
    res = cur2.execute('SELECT * FROM adherent')
    con2.commit()

    name = res.fetchall()
    return render(response, 'ping/base.html', {"name": name})

def home(response):
    return render(response, 'ping/home.html', {})

@csrf_exempt
def livre(request):
    liste=[]
    data = request.POST
    isbn_data = data.get("isbn", "")

    con = sqlite3.connect("bibliotheque.db", )

    isbn=isbn_data

    book = isbnlib.meta(isbn)
    author_data = str(book.get('Authors'))[2:-2]
    title_data = str(book.get('Title'))
    publisher_data = str(book.get('Publisher'))
    
    author=author_data
    title=title_data
    publisher=publisher_data
    if isbn_data == '':
        pass
    else:
        res ='INSERT OR REPLACE INTO livre(isbn, titre, auteur, editeur) VALUES ("'+isbn+'","'+title+'","'+author+'","'+publisher+'")'
        cur = con.cursor()
        cur.execute(res)
        
        con.commit()

    cur = con.cursor()
    res2 = cur.execute("SELECT * FROM livre")
    con.commit()

    livre_liste = res2.fetchall()

    for item in res2.fetchall():
        liste.append(item)

    if data == {}:
        value = ""
    else:
        value = livre_liste[-1][1]

    con.commit()

    return render(request, 'ping/livre.html', {"livre": livre_liste, "item": value})

@csrf_exempt
def add(request):
    liste=[]
    id = str(uuid.uuid4())[:8]
    data = request.POST
    print(data)
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
        res ='INSERT OR REPLACE INTO adherent(nomAdherent, prenomAdherent, adresse, telephone, mdp) VALUES ("'+nom+'","'+prenom+'", "'+adresse+'","'+tel+'","'+id+'")'
        cur = con.cursor()
        cur.execute(res)
        
        con.commit()

    cur = con.cursor()
    res3 = cur.execute("SELECT * FROM adherent")
    con.commit()

    for item in res3.fetchall():
        liste.append(item)

    if data == {}:
        value = ""
    else:
        value = liste[-1][1]

    return render(request, 'ping/add.html', {"item": value, "adherent_liste": liste})

@csrf_exempt
def delete(request):
    book_delete=[]
    data = request.POST
    id_data = data.get("id", "")
    book_data = data.get("book", "")

    identifiant=id_data
    book_id=book_data


    requete="delete from adherent where mdp =:identifiant"
    requete2="delete from livre where isbn =:isbn"
    
    con = sqlite3.connect("bibliotheque.db")

    cur = con.cursor()
    res2 = "SELECT * FROM adherent where mdp =:identifiant"

    test5 = cur.execute(res2,{"identifiant":identifiant})

    value = test5.fetchall()

    isbn=book_id
    con2 = sqlite3.connect("bibliotheque.db")
    cur2 = con2.cursor()
    res = cur2.execute('SELECT * FROM livre WHERE isbn=?', [isbn] )
    test3 = res.fetchall()
    con2.commit()
    

    if value == []:
        value = ""
    else:
        value = value[0][1]

    if test3 == []:
        book_delete = ""
    else:
        for item in test3:
            book_delete.append(item)

        book_delete = book_delete[0][1]

    cur.execute(requete,{"identifiant":identifiant})
    cur.execute(requete2,{"isbn":book_id})

    con.commit()

    return render(request, 'ping/delete.html', {"item": value, "item_book": book_delete})
    
@csrf_exempt
def emprunts(request):
    data = request.POST
    isbn_data = data.get("isbn", "")

    # con = sqlite3.connect("bibliotheque.db", )

    isbn=isbn_data

    print(isbn)
    
    return render(request, 'ping/emprunts.html', {})