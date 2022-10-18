from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import isbnlib 
import uuid

from datetime import date, timedelta





def index(response):

    return render(response, 'ping/base.html')

def home(response):
    return render(response, 'ping/home.html', {})

@csrf_exempt
def livre(request):
    liste=[]
    # liste4=[]
    data = request.POST
    isbn_data = data.get("isbn", "")

    con = sqlite3.connect("bibliotheque.db", )

    isbn=isbn_data

    cover2 = isbnlib.cover(isbn)

    cover="https://covers.openlibrary.org/b/isbn/{}-L.jpg".format(isbn)

    import requests
    img_size = requests.get(cover).content
    

    if len(img_size) == 807:
        cover3=cover2.get('thumbnail')  # type: ignore
    else:
        cover3="https://covers.openlibrary.org/b/isbn/{}-L.jpg".format(isbn)

   

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

    return render(request, 'ping/livre.html', {"livre": livre_liste, "item": value, "cover": cover3})

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
    member_del=[]
    data = request.POST
    id_data = data.get("id", "")
    book_data = data.get("book", "")

    identifiant=id_data
    book_id=book_data

    requete="delete from adherent where mdp =:identifiant"
    requete2="delete from livre where isbn =:isbn"

    con = sqlite3.connect("bibliotheque.db")

    cur = con.cursor()
    

    isbn=book_id
    con2 = sqlite3.connect("bibliotheque.db")
    cur2 = con2.cursor()
    res = cur2.execute('SELECT * FROM livre WHERE isbn=?', [isbn] )
    res9 = cur2.execute("SELECT * FROM adherent where mdp =?", [identifiant])

    test5 = res9.fetchall()
    test3 = res.fetchall()
    
    con2.commit()
    

    if test5 == []:
        member_del = ""
    else:
        for item in test5:
            member_del.append(item)

        member_del = member_del[0][1]
    
    print(member_del)

    if test3 == []:
        book_delete = ""
    else:
        for item in test3:
            book_delete.append(item)

        book_delete = book_delete[0][1]

    cur.execute(requete,{"identifiant":identifiant})
    cur.execute(requete2,{"isbn":book_id})

    con.commit()

    return render(request, 'ping/delete.html', {"item": member_del, "item_book": book_delete})
    
@csrf_exempt
def emprunts(request):
    liste = []
    data = request.POST
    isbn_data = data.get("isbn", "")
    member_data = data.get("prenom", "")

    con = sqlite3.connect("bibliotheque.db", )

    isbn=isbn_data
    member=member_data


    book = isbnlib.meta(isbn)
    title_data = str(book.get('Title'))

    
    
    cur = con.cursor()
    res4 = cur.execute('SELECT * FROM livre WHERE isbn=?', [isbn] )
    res5 = cur.execute('SELECT * FROM adherent WHERE mdp=?', [member] )
    
    test3 = res4.fetchall()
    test9 = res5.fetchall()
    con.commit()

    

    today_date = date.today()
    td = timedelta(-42)
     

    title=title_data
    date_emprunt=str(today_date)
    date_retour=str(today_date+td)
    if isbn_data == '' and member_data == '':
        pass
    else:
        if test3 == [] and test9 == []:
            pass
        else:
            res ='INSERT OR REPLACE INTO emprunt(isbn, identifiant, dateemprunt, dateretour) VALUES ("'+isbn+'","'+member+'","'+date_emprunt+'","'+date_retour+'")'
            cur = con.cursor()
            cur.execute(res)
            
            con.commit()

    cur = con.cursor()
    res2 = cur.execute("SELECT * FROM emprunt")
    con.commit()

    livre_liste = res2.fetchall()

    for item in res2.fetchall():
        liste.append(item)

    if data == {}:
        value = ""
        title = ""
    else:
        if test3 == []:
            value = ""
            title = ""
        else:
            value = livre_liste[-1][1] + " / "

    con.commit()

    return render(request, 'ping/emprunts.html', {"item": value, "liste_emprunts": livre_liste, "title": title})


@csrf_exempt
def retard(request):
    retour_loan=[]
    data = request.POST

    isbn_data = data.get("isbn", "")
    member_data = data.get("prenom", "")

    requete3="delete from emprunt where isbn =:isbn and identifiant =:prenom"
    requete2="delete from retour where identifiant > 0"

    con = sqlite3.connect("bibliotheque.db")

    cur = con.cursor()
    cur3 = con.cursor()

    cur.execute(requete3,{"isbn":isbn_data, "prenom":member_data})
    cur3.execute(requete2)

    today_date = date.today()
    # td = timedelta(-42)

    con3 = sqlite3.connect("bibliotheque.db")
    cur3 = con3.cursor()
    res6 = cur3.execute('SELECT * FROM emprunt WHERE isbn="%s" AND identifiant="%s"' % (isbn_data,member_data))
    con3.commit()
    test7 = res6.fetchall()


    con5 = sqlite3.connect("bibliotheque.db")
    cur5 = con5.cursor()
    res10 = cur5.execute('SELECT isbn, identifiant, dateretour FROM emprunt WHERE dateretour < ?', [today_date])
    test12 = res10.fetchall()
    con5.commit()
    

    print(test12)

    book = isbnlib.meta(isbn_data)
    title_data = str(book.get('Title'))


    title=title_data
    if data == {}:
        retour_loan = ""
        title = ""
    else:
        if test7 == []:
            retour_loan = ""
            title = ""
        else:
            for item in test7:
                retour_loan.append(item)

            res11 = cur5.execute('SELECT * FROM emprunt WHERE dateretour < ?', [today_date])
            test12 = res11.fetchall()
            con5.commit()

            retour_loan = retour_loan[0][1] + " / "

    con.commit()

    return render(request, 'ping/retard.html', {"item_loan": retour_loan, "title": title, "delay": test12})