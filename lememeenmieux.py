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


#Main loop
stay=1
while (stay):
    #Interaction with the user
    print("\n\nLe même en mieux : faites vous plaisir tout en mangeant mieux.\n\n")
    print("Faites votre choix:\n")
    print("1) Rechercher une catégorie")
    print("2) Afficher les recherches sauvegardées")
    print("3) Effacer les recherches sauvegardées\n")
    #c.execute("""SELECT (id,CategoryName) FROM Categories""")
    menu = input("Entrez 1, 2 ou 3: ")

    while menu not in ["1","2","3"]:
        print("Saisie incorrecte !")
        menu = input("Entrez 1, 2 ou 3: ")
        
    if (menu == "2"):
        c.execute("""SELECT ProductName,SubName from Substitutes ORDER BY id """)
        subaslist=list(c.fetchall())

        print("Choisissez parmi les produits suivants :")
        #print(cat_list)
        #print(prod_list)

        sub_id_list=[0]
        new_id_sub=1
        for elt in subaslist:
            #print(" ",eltp[0]," - ",eltp[1])
            print(" ",new_id_sub," - ",elt[1],"peut remplacer",elt[0])
            sub_id_list.append(new_id_sub)
            new_id_sub+=1

        choice=1000
        while (choice not in sub_id_list):
            print("Entrez 0 pour revenir au menu")
            menu_sub = input("Ou entrez le numéro d'une alternative pour avoir plus d'infos : ")
            try:
                choice=int(menu_sub)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")
                        
        
        if choice == 0:
            pass
        else:
            sub_choice = subaslist[choice-1][1]
            c.execute("""SELECT Places,Stores,Link from Products WHERE ProductName like %s """,(sub_choice,))

            infoaslist=list(c.fetchone())
            print("Nom de l'alternative :",sub_choice)
            print("Pays ou Ville :",infoaslist[0])
            print("Lieu de Vente :",infoaslist[1])
            print("Plus d'info ici :",infoaslist[2])
            
    elif (menu == "3"):
        c.execute("""TRUNCATE TABLE Substitutes;""")

           
    elif (menu =="1"):
        print("Choisissez parmi les catégories suivantes :")

        #print(cat_list)
        #print(prod_list)

        cat_id_list=[]
        for elt in cat_list:
            print(" ",elt[0]," - ",elt[1])
            cat_id_list.append(elt[0])

        print(cat_id_list)
        #cat_num = input("Entrez le numéro d'une catégorie : ")

        #while (cat_num is not [0..9]) or (int(cat_num) not in cat_id_list) :
        #    print("Saisie incorrecte !")
        #    raise Warning("Entrez le numéro d'une catégorie : ")

        choice=0
        while (choice not in cat_id_list):
            cat_num = input("Entrez le numéro d'une catégorie : ")
            try:
                choice=int(cat_num)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")
        
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
        #prod_num = int(input("Entrez le numéro d'un produit: "))

        #while prod_num not in prod_id_list :
        #    raise Warning("Saisie incorrecte !")
        #    prod_num = int(input("Entrez le numéro d'un produit: "))

        choice=0
        while (choice not in prod_id_list):
            prod_num = input("Entrez le numéro d'un produit : ")
            try:
                choice=int(prod_num)
            except EOFError as e:
                print("Saisie incorrecte !")
            except ValueError as v:
                print("Saisie incorrecte !")

                
        prod_choice = prod_list[int(prod_num)-1][1]
        print("Votre choix est", prod_choice)

        #c.execute("""SELECT * from products WHERE CategoryName like %s AND ProductName not like %s ORDER BY id """,(cat_choice,prod_choice))
        c.execute("""SELECT * from products WHERE CategoryName like %s ORDER BY Grade """,(cat_choice,))

        sub_list=list(c.fetchall())
        print("Voici la liste des produits :")
        print(sub_list)

        sub_exists=0
        candidate_list=[]
        for candidate in sub_list:
            clist=list(candidate)
            print(clist)
            if (clist[1] == prod_choice):
                break
            else:
                candidate_list.append(clist[1])
                sub_exists=1
        if sub_exists:        
            print("Voici la liste des alternatives :")
            print(candidate_list)

            print("Voici la meilleure alternative à votre produit :")
            print(candidate_list[0])

            print("Voulez-vous voir afficher les infos relatives à cette alternative ?")
            moreinfo = input(" 1-Oui 2-Non : ")

            while moreinfo not in ["1","2"]:
                print("Saisie incorrecte !")
                moreinfo = input("Entrez 1 ou 2 : ")
                
            if (moreinfo == "2"):
                pass
            elif (moreinfo =="1"):
                c.execute("""SELECT Places,Stores,Link from Products WHERE ProductName like %s """,(candidate_list[0],))

                infoaslist=list(c.fetchone())
                print("Nom de l'alternative :",candidate_list[0])
                print("Pays ou Ville :",infoaslist[0])
                print("Lieu de Vente :",infoaslist[1])
                print("Plus d'info ici :",infoaslist[2])
        
            print("Voulez-vous sauvegarder ce résultat ? ")
            save = input(" 1-Oui 2-Non : ")

            while save not in ["1","2"]:
                print("Saisie incorrecte !")
                save = input("Entrez 1 ou 2 : ")
                
            if (save == "2"):
                pass
            elif (save =="1"):
                print("Sauvegarde en cours pour le couple ",prod_choice,"/",candidate_list[0])
                c.execute("""INSERT INTO Substitutes (ProductName,SubName) VALUES (%s,%s)""",(prod_choice,candidate_list[0],))
                print("Alternative sauvegardée ! ")
                

        print("Revenir au menu principal ?")
        print("1-oui      2-quitter le programme")
        back=input("Votre choix : ")
        
        while back not in ["1","2"]:
            print("Saisie incorrecte !")
            back = input("Entrez 1 ou 2 : ")
            
        if (back == "1"):
            pass
        elif (back =="2"):
            stay=0
                
        """
        for elt in sub_list:
            elt_list=list(elt)
            grade=elt_list[5]
            if (elt_list[5] == "a"):
                elt_list[5]=1
            if (elt_list[5] == "b"):
                elt_list[5]=2
            if (elt_list[5] == "c"):
                elt_list[5]=3
            if (elt_list[5] == "d"):
                elt_list[5]=4
            else:
                elt_list[5]=5
        
        """
        
        #sub_tup=c.fetchone()
        #print(sub_tup)
"""
        if (sub_tup is None ):
            print("Malheureusement, il n'y a aucun substitut au produit que vous avez choisi. ")
            
        else:
            sub_list=list(sub_tup)
            print("Voici un substitut au produit que vous avez choisi :")
            print(sub_list[1])

            print("Voulez-vous sauvegarder ce résultat ? ")
            save = input(" 1-Oui 2-Non : ")

            while save not in ["1","2"]:
                print("Saisie incorrecte !")
                save = input("Entrez 1 ou 2 : ")
                
            if (save == "2"):
                pass
            elif (save =="1"):
"""
#                c.execute("""INSERT INTO Substitutes (ProductName,SubName) VALUES (%s,%s)""", (prod_choice,sub_list[1],))
#                print("Substitut sauvegardé ! ")
"""
        print("Revenir au menu principal ?")
        print("1-oui      2-quitter le programme")
        back=input("Votre choix : ")
        while back not in ["1","2"]:
            print("Saisie incorrecte !")
            back = input("Entrez 1 ou 2 : ")
            
        if (back == "1"):
            pass
        elif (back =="2"):
            stay=0
 """


db.commit()


