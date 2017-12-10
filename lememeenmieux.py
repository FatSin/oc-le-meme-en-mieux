import MySQLdb
import json

"""

"""


#Connection to openfood db (The password will be stored in another file later !!)
db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

c=db.cursor()
#Retrieve of DB data as lists


c.execute('SELECT * from categories ORDER BY id;')
cat_tup=c.fetchall()
cat_list=list(cat_tup)

c.execute('SELECT * from products ORDER BY id;')
prod_tup=c.fetchall()
prod_list=list(prod_tup)

#r=db.store_result()
#cat_result=r.fetch_row()




#Interaction with the user
print("Le même en mieux : faites vous plaisir tout en mangeant mieux.")
print("Faites votre choix:")
print("1) Rechercher une catégorie")
print("2) Afficher les recherches sauvegardées")
#c.execute("""SELECT (id,CategoryName) FROM Categories""")
menu = input("Entrez 1 ou 2 : ")

while menu not in ["1","2"]:
    print("Saisie incorrecte !")
    menu = input("Entrez 1 ou 2 : ")
    
if (menu == "1"):
    print("Cette fonctionnalité n'est pas encore implémentée")
elif (menu =="2"):
    print("Choisissez parmi les catégories suivantes :")

    #print(cat_list)
    #print(prod_list)

    cat_id_list=[]
    for elt in cat_list:
        print(" ",elt[0]," - ",elt[1])
        cat_id_list.append(elt[0])

    print(cat_id_list)
    cat_num = input("Entrez le numéro d'une catégorie : ")

    while (cat_num is not [0..9]) or (int(cat_num) not in cat_id_list) :
        print("Saisie incorrecte !")
        cat_num = input("Entrez le numéro d'une catégorie : ")
    
    
    cat_choice = cat_list[int(cat_num)-1][1]
    print("Votre choix est", cat_choice)


    c.execute("""SELECT * from products WHERE CategoryName like %s ORDER BY id """,(cat_choice,))
    prod_tup=c.fetchall()
    prod_list=list(prod_tup)


    print("Choisissez parmi les produits suivants :")
    #print(cat_list)
    #print(prod_list)

    prod_id_list=[]
    new_id_prod=1
    for eltp in prod_list:
        #print(" ",eltp[0]," - ",eltp[1])
        print(" ",new_id_prod," - ",eltp[1])
        prod_id_list.append(new_id_prod)
        new_id_prod+=1
        

    print(prod_id_list)
    prod_num = int(input("Entrez le numéro d'un produit: "))

    while prod_num not in prod_id_list :
        print("Saisie incorrecte !")
        prod_num = int(input("Entrez le numéro d'un produit: "))


    prod_choice = prod_list[int(prod_num)-1][1]
    print("Votre choix est", prod_choice)

    c.execute("""SELECT * from products WHERE CategoryName like %s AND ProductName not like %s ORDER BY id """,(cat_choice,prod_choice))
    sub_tup=c.fetchone()
    print(sub_tup)

    if (sub_tup is None ):
        print("Malheureusement, il n'y a aucun substitut au produit que vous avez choisi. ")
    else:
        sub_list=list(sub_tup)
        print("Voici un substitut au produit que vous avez choisi :")
        print(sub_list[1])

        print("Voulez-vous sauvegarder ce résultat ? ")
        save = input(" 1-Oui 2-Non : ")
        if (save == "1"):
            print("Substitut sauvegardé ! ")

            c.execute("""INSERT INTO Substitutes (ProductName,SubName) VALUES (%s,%s)""", (prod_choice,sub_list[1],))
            
        elif (save =="2"):
            print("Retour au menu :")
        else:
            print("Choix incorrect, veuillez refaire votre saisie.")


else:
    print("Choix incorrect, veuillez refaire votre saisie.")

db.commit()
