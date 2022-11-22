from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import isbnlib 
import uuid
import requests
from datetime import date, timedelta

# HOME PAGE
def home(response):
    return render(response, 'ping/home.html') # Display the main page of the website

# LIST OF BOOK AND ADD BOOK
@csrf_exempt
def book(request):
    # Connect to the database
    con = sqlite3.connect("bibliotheque.db", ) 
    cur = con.cursor()

    id = str(uuid.uuid4())[:8] # 8-digit random number for the added book identifier

    data = request.POST # Return the POST value on the book.html page 
    isbn_data = data.get("isbn", "") # Select the ISBN value in a form with id='isbn'

    cover_isbnlib = isbnlib.cover(isbn_data) # Return the book cover with isbnlib data

    cover_openlibrary="https://covers.openlibrary.org/b/isbn/{}-L.jpg".format(isbn_data) # URL to return the book cover on openlibrery with isbn
    img_size = requests.get(cover_openlibrary).content # Return the weight of the content as kb

    if len(img_size) == 807: # The weight of a null content is 807 kb, when there is no image 
        cover_img=cover_isbnlib.get('thumbnail')  # type: ignore // Selection of the book cover with the best quality
    else:
        cover_img=cover_openlibrary 

    # Variable for book information with isbnlib data
    book = isbnlib.meta(isbn_data)
    author_data = str(book.get('Authors'))[2:-2]
    title_data = str(book.get('Title'))
    publisher_data = str(book.get('Publisher'))
    
    # Add the book data to the database with SQLite
    if isbn_data == '':
        pass
    else:
        # Commands for the insertion of a value in the database
        res_add_livre ='INSERT OR REPLACE INTO livre(mdp, isbn, titre, auteur, editeur, emprunt) VALUES ("'+id+'","'+isbn_data+'","'+title_data+'","'+author_data+'","'+publisher_data+'",0)'
        cur.execute(res_add_livre)
        con.commit() 

    # Select all books data with SQLite
    res__select_livre = cur.execute("SELECT * FROM livre")
    con.commit()

    # Add all values in the list to be displayed on the page
    livre_liste=[]
    for item in res__select_livre.fetchall():
        livre_liste.append(item)

    # Return the new book inserted in the database to display it on the page
    if data == {}:
        value_new_livre = ""
    else:
        value_new_livre = livre_liste[-1][1]

    con.commit()
    con.close()

    return render(request, 'ping/book.html', {"livre": livre_liste, "item": value_new_livre, "cover": cover_img}) # Send the variables that appear on the page with {"variable_name_page": variable_name_program}

# ADD MEMBER
@csrf_exempt
def add(request):
    # Connect to the database
    con = sqlite3.connect("bibliotheque.db")
    cur = con.cursor()
    
    id = str(uuid.uuid4())[:8] # 8-digit random number for the added member identifier

    data = request.POST # Return the POST value on the add.html page 

    # Variable for member information with form data
    nom_data = data.get("nom", "")
    prenom_data = data.get("prenom", "")
    adresse_data = data.get("adresse", "")
    tel_data = data.get("tel", "")

    # Add the member data to the database with SQLite
    if nom_data == '' or prenom_data == "" or adresse_data == "" or tel_data == "":
        pass
    else:
        # Commands for the insertion of a value in the database
        res_add_adherent ='INSERT OR REPLACE INTO adherent(nomAdherent, prenomAdherent, adresse, telephone, mdp) VALUES ("'+nom_data+'","'+prenom_data+'", "'+adresse_data+'","'+tel_data+'","'+id+'")'
        cur.execute(res_add_adherent)
        con.commit()

    # Select all members data with SQLite
    res_select_adherent = cur.execute("SELECT * FROM adherent")
    con.commit()
  
    # Add all values in the list to be displayed on the page
    liste_adherent=[]
    for item in res_select_adherent.fetchall():
        liste_adherent.append(item)

    # Return the new member inserted in the database to display it on the page
    if data == {}:
        value_new_adherent = ""
    else:
        value_new_adherent = liste_adherent[-1][1]

    return render(request, 'ping/add.html', {"item": value_new_adherent, "adherent_liste": liste_adherent}) # Send the variables that appear on the page with {"variable_name_page": variable_name_program}

# DELETE BOOK AND MEMBER
@csrf_exempt
def delete(request):
    con = sqlite3.connect("bibliotheque.db")
    cur = con.cursor()

    book_delete=[]
    member_delete=[]
    liste_emprunts=[]
    liste_book=[]

    data = request.POST
    id_data = data.get("id", "")
    isbn_data = data.get("book", "")

    con_verify_adherent = sqlite3.connect("bibliotheque.db")
    cur_verify_adherent = con_verify_adherent.cursor()
    res_verify_adherent = cur_verify_adherent.execute('SELECT identifiant FROM emprunt')

    con_verify_book = sqlite3.connect("bibliotheque.db")
    cur_verify_book = con_verify_book.cursor()
    res_verify_book = cur_verify_book.execute('SELECT mdp FROM emprunt')

    con_verify_book.commit()

    for item in res_verify_adherent.fetchall():
        liste_emprunts.append(str(item))

    for item in res_verify_book.fetchall():
        liste_book.append(str(item))

    print(liste_book)
    print("('"+isbn_data+"',)")

    delete_impossible = ""

    if "('"+id_data+"',)" in liste_emprunts:
        member_delete = "Impossible: Cet adherent a un livre"
    else:
        res_delete_livre="delete from livre where mdp =:isbn"


        res_delete_adherent="delete from adherent where mdp =:identifiant"

        con_select_adherent = sqlite3.connect("bibliotheque.db")
        cur_select_adherent = con_select_adherent.cursor()
        res_select_adherent = cur_select_adherent.execute('SELECT * FROM adherent WHERE mdp="%s"' % id_data)
        retour2 = res_select_adherent.fetchall()


        con_select_adherent.commit()

        if data == {}:
            member_delete = ""
        else:
            if retour2 == []:
                member_delete = ""
            else:
                for item in retour2:
                    member_delete.append(item)

                member_delete = member_delete[0][1]

        cur.execute(res_delete_adherent,{"identifiant":id_data})
        con.commit()

    if "('"+isbn_data+"',)" in liste_book:
        book_delete = "Impossible: Ce livre est emprunté"
    else:
    
        con_select_livre = sqlite3.connect("bibliotheque.db")
        cur_select_livre = con_select_livre.cursor()
        res_select_livre = cur_select_livre.execute('SELECT * FROM livre WHERE mdp="%s"' % isbn_data)
        con_select_livre.commit()
        retour = res_select_livre.fetchall()

        if data == {}:
            book_delete = ""
        else:
            if retour == []:
                book_delete = ""
            else:
                for item in retour:
                    book_delete.append(item)

                book_delete = book_delete[0][2]
                cur.execute(res_delete_livre,{"isbn":isbn_data})
                con.commit()

        con.close()

    return render(request, 'ping/delete.html', {"item": member_delete, "item_book": book_delete, "impossible": delete_impossible})
    
# BORROW BOOK
@csrf_exempt
def emprunts(request):
    con = sqlite3.connect("bibliotheque.db", )
    con2 = sqlite3.connect("bibliotheque.db", )
    con3 = sqlite3.connect("bibliotheque.db", )

    today_date = date.today()
    td = timedelta(-42)
    date_emprunt=str(today_date)
    date_retour=str(today_date+td)

    liste_emprunts = []
    livre_liste = []
    liste_verify=[]

    data = request.POST
    isbn_data = data.get("isbn", "")
    member_data = data.get("prenom", "")

    cur = con.cursor()
    cur3 = con3.cursor()
    cur2 = con2.cursor()
    
    res_select_livre = cur2.execute('SELECT * FROM livre WHERE isbn=?', [isbn_data] )
    con2.commit()

    for item in res_select_livre.fetchall():
        livre_liste.append(item)
    
    emprunt_impossible = ""

    if data == {}:
        id_livre = ""
        emprunt_impossible = ""
    else:
        for i in range(len(livre_liste)):
            if livre_liste[i][-1] == 0:
                id_livre = livre_liste[i][0]
                print(id_livre)
                break
            else:
                if livre_liste[i][0] == livre_liste[-1][0]:
                    emprunt_impossible = "Impossible: Livre indisponible"
                    break
                else:
                    pass

    con2.commit()

    

    res_select_adherent = cur.execute('SELECT * FROM adherent WHERE mdp=?', [member_data] )
    res_verify_adherent = cur3.execute('SELECT  isbn FROM emprunt WHERE identifiant=?', [member_data] )
    for item in res_verify_adherent.fetchall():
        liste_verify.append(str(item))

    con3.close()
    

    book = isbnlib.meta(isbn_data)
    title_data = str(book.get('Title'))

    if isbn_data == '' and member_data == '':
        pass
    else:
        if res_select_livre.fetchall() == [] and res_select_adherent.fetchall() == []:
            pass
        else:
            
            if emprunt_impossible == "":
                
                if "('"+isbn_data+"',)" in liste_verify:
                    emprunt_impossible = "Impossible: Livre déjà emprunté"
                else:   
                    res ='INSERT OR REPLACE INTO emprunt(isbn, identifiant, dateemprunt, dateretour, mdp) VALUES ("'+isbn_data+'","'+member_data+'","'+date_emprunt+'","'+date_retour+'","'+str(id_livre)+'")'
                    cur = con.cursor()
                    cur.execute(res)
                        
                    con.commit()
            

    cur = con.cursor()
    res_select_emprunts = cur.execute("SELECT * FROM emprunt")
    con.commit()
    
    for item in res_select_emprunts.fetchall():
        liste_emprunts.append(item)

    if data == {}:
        value_new_emprunt = ""
        title_data = ""
    else:
        if res_select_livre.fetchall() == []:
            value_new_emprunt = ""
            title_data = ""
        else:
            value_new_emprunt = liste_emprunts[-1][1] + " / "

    

    if emprunt_impossible == "":
        cur.execute('UPDATE livre set emprunt = 1 WHERE mdp="%s"' % id_livre)

    con.commit()
    con.close()

    return render(request, 'ping/emprunts.html', {"item": value_new_emprunt, "liste_emprunts": liste_emprunts, "title": title_data, "erreur": emprunt_impossible})

# LIST OF DELAYS
@csrf_exempt
def retard(request):
    con = sqlite3.connect("bibliotheque.db")

    today_date = date.today()

    retour_loan=[]

    data = request.POST
    isbn_data = data.get("isbn", "")
    member_data = data.get("prenom", "")

    cur = con.cursor()
    cur.execute("delete from retour where isbn > 0")
    res = cur.execute('SELECT isbn, identifiant, dateretour FROM emprunt WHERE dateretour < ?', [today_date])
    test = res.fetchall()

    for i in range(len(test)):
        cur.execute('INSERT OR REPLACE INTO retour(isbn, identifiant, dateretard) VALUES("'+str(test[i][0]) +'","'+ str(test[i][1]) +'","'+ str(test[i][2])+'")')
    con.commit()

    book = isbnlib.meta(isbn_data)
    title_data = str(book.get('Title'))

    con_retour = sqlite3.connect("bibliotheque.db")
    cur_retour = con_retour.cursor()
    res_retour = cur_retour.execute('SELECT * FROM emprunt WHERE isbn="%s" AND identifiant="%s"' % (isbn_data,member_data))
    con_retour.commit()
    retour = res_retour.fetchall()

    value_retour_loan=""

    if data == {}:
        retour_loan = ""
        title_data = ""
    else:
        if retour == []:
            retour_loan = ""
            title_data = ""
        else:
            for item in retour:
                retour_loan.append(item)

            value_retour_loan = retour_loan[0][1] + " / "

    if isbn_data == '':
        pass
    else:
        con_retard = sqlite3.connect("bibliotheque.db")
        cur_retard = con_retard.cursor()
        cur_retard.execute('UPDATE livre set emprunt = 0 WHERE mdp="%s"' % retour_loan[0][-1] )
        cur_retard.execute('DELETE FROM emprunt WHERE isbn="%s" AND identifiant="%s"' % (isbn_data,member_data))
        cur_retard.execute('DELETE FROM retour WHERE isbn="%s" AND identifiant="%s"' % (isbn_data,member_data))
        
        con_retard.commit()

    res_retard = cur.execute("SELECT * FROM retour")
    con.commit()
    value_retard = res_retard.fetchall()

    con.close()

    return render(request, 'ping/retard.html', {"item_loan": value_retour_loan, "title": title_data, "delay": value_retard})