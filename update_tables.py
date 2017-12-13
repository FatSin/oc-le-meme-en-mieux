import requests
import MySQLdb
import json
import re

"""
    Script for the creation and population of Openfood local db's tables,
    from online data. The db must be created (no data necesary) before launching the script.
"""


#HTTP Requests To Retrieve the 1st 3 pages of the products sold in France
req1 = requests.get('https://world.openfoodfacts.org/country/france.json')
req2 = requests.get('https://world.openfoodfacts.org/country/france/2.json')
req3 = requests.get('https://world.openfoodfacts.org/country/france/3.json')
req4 = requests.get('https://world.openfoodfacts.org/country/france/4.json')
req5 = requests.get('https://world.openfoodfacts.org/country/france/5.json')

#Conversion of HTTP content into json, and utf8-decoding to avoid charset conflicts due to FR characters
data1 = json.loads(req1.content.decode('utf-8'))
data2 = json.loads(req2.content.decode('utf-8'))
data3 = json.loads(req3.content.decode('utf-8'))
data4 = json.loads(req4.content.decode('utf-8'))
data5 = json.loads(req5.content.decode('utf-8'))

data = [data1, data2, data3, data4, data5]

#Connection to openfood db (The password will be stored in another file later !!)
db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

c=db.cursor()


#Decoding to avoid charset conflicts due to FR characters, again
db.set_character_set('utf8')
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')


#Erase the existing tables
#c.execute("""DROP TABLE IF EXISTS Substitutes """)
#c.execute("""DROP TABLE IF EXISTS Products """)
#c.execute("""DROP TABLE IF EXISTS Categories """)

c.execute("""ALTER TABLE Substitutes
            DROP FOREIGN KEY sub_k""")
c.execute("""ALTER TABLE Products
            DROP FOREIGN KEY prod_k""")

c.execute('TRUNCATE TABLE Substitutes;')
c.execute('TRUNCATE TABLE  Products;')
c.execute('TRUNCATE TABLE  Categories;')

c.execute("""ALTER TABLE Products
            ADD CONSTRAINT prod_k FOREIGN KEY (id) REFERENCES Categories (id)""")
c.execute("""ALTER TABLE Substitutes
            ADD CONSTRAINT sub_k FOREIGN KEY (id) REFERENCES Products (id)""")

#Creation of Categories and Products tables -> handled by .sql script
#c.execute("""CREATE TABLE IF NOT EXISTS Categories (
#    id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
#    CategoryName VARCHAR(40) UNIQUE NOT NULL)""")
	
#c.execute("""CREATE TABLE IF NOT EXISTS Products (
 #   id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  #  ProductName VARCHAR(40) UNIQUE NOT NULL,
   # CategoryName VARCHAR(40) NOT NULL,
#    Places VARCHAR(40),
#    Stores VARCHAR(40),
#    Grade VARCHAR(1) NOT NULL)""")

#c.execute("""CREATE TABLE IF NOT EXISTS Substitutes (
#    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    ProductName VARCHAR(40) NOT NULL,
#    SubName VARCHAR(40) NOT NULL,
#    purchase_places VARCHAR(40),
#    stores VARCHAR(40))""")

#c.execute("""CREATE TABLE IF NOT EXISTS Products (
#    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
#    ProductName VARCHAR(40) UNIQUE NOT NULL,
#    CategoryName VARCHAR(40) NOT NULL,
#    Places VARCHAR(40),
#    Stores VARCHAR(40),
#    Grade VARCHAR(1),
#    CONSTRAINT fk_catname
#      FOREIGN KEY (CategoryName)
#      REFERENCES Categories(CategoryName))""")

#Population of the tables with HTTP content
cat_id=1
for element in data:
    for entry in element["products"]:
        #Check the presence of critical keys/columns
        if ("categories" in entry.keys() and "product_name" in entry.keys() and "nutrition_grade_fr" in entry.keys()):
            if (entry["categories"] == '' or entry["product_name"] == ''):
                print("Rejeté car nul : - categorie : ",entry["categories"],"et produit",entry["product_name"])
                #pass
                #print("cette cat est vide!")
            else:
                #Retrieve the French name of the category
                cat_split = entry["categories"].split(',')
                r=re.compile("fr*")
                cat_new=filter(r.match,cat_split)
                cat_short=list(cat_new)
                if (cat_short == []):
                    cat_fin=cat_split[0]
                else:
                    cat_fin=cat_short[0][3:]
                
                prod_short = entry["product_name"][:25]

                print("Ajout en cours : - categorie : ",cat_fin,"et produit",prod_short)

                c.execute("""SELECT * FROM Categories WHERE CategoryName like %s""", (cat_fin,))
                cat_list=list(c.fetchall())
                #print("Il y a déjà", len(cat_list),"occurrences pour la catégorie",cat_short[0])
                
                c.execute("""INSERT IGNORE INTO Categories (id,CategoryName) VALUES (%s,%s)""", (cat_id,cat_fin,))

                if ("stores" in entry.keys() and "purchase_places" and "url" in entry.keys()):
                    c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade,Places,Stores,Link) VALUES (%s,%s,%s,%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],entry["purchase_places"],entry["stores"],entry["url"],))
                    print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                else:
                    c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade) VALUES (%s,%s,%s)""", (prod_short,cat_fin,entry["nutrition_grade_fr"],))

                print("Ce produit est ajouté :", entry["product_name"])
                
                if (len(cat_list) == 0):
                   cat_id+=1 
                
                #Import location of the products, if it exists
                #print("stores, place et url :", entry["stores"], entry["purchase_places"], entry["url"])
                #if ("stores" in entry.keys() and "purchase_places" and "url" in entry.keys()):
                    #c.execute("""INSERT INTO Products (Places,Stores,Link) VALUES (%s,%s,%s)""", (entry["purchase_places"],entry["stores"],entry["url"],))                
        else:
            print("Keys pas bonnes!!")


db.commit()
