import requests
import MySQLdb
import json

"""
    Script for the creation and population of Openfood local db's tables,
    from online data. The db must be created (no data necesary) before launching the script.
"""


#HTTP Requests To Retrieve the 1st 3 pages of the products sold in France
req1 = requests.get('https://world.openfoodfacts.org/country/france.json')
req2 = requests.get('https://world.openfoodfacts.org/country/france/2.json')
req3 = requests.get('https://world.openfoodfacts.org/country/france/3.json')

#Conversion of HTTP content into json, and utf8-decoding to avoid charset conflicts due to FR characters
data1 = json.loads(req1.content.decode('utf-8'))
data2 = json.loads(req2.content.decode('utf-8'))
data3 = json.loads(req3.content.decode('utf-8'))

data = [data1, data2, data3]

#Connection to openfood db (The password will be stored in another file later !!)
db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

c=db.cursor()


#Decoding to avoid charset conflicts due to FR characters, again
db.set_character_set('utf8')
c.execute('SET NAMES utf8;')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')


#Erase the existing tables
c.execute("""DROP TABLE IF EXISTS Products """)
c.execute("""DROP TABLE IF EXISTS Categories """)

#Creation of Categories and Products tables
c.execute("""CREATE TABLE IF NOT EXISTS Categories (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(40) UNIQUE NOT NULL)""")
	
c.execute("""CREATE TABLE IF NOT EXISTS Products (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(40) UNIQUE NOT NULL,
    CategoryName VARCHAR(40) UNIQUE NOT NULL,
    Places VARCHAR(40),
    Stores VARCHAR(40),
    Grade VARCHAR(1),
    CONSTRAINT fk_catname
      FOREIGN KEY (CategoryName)
      REFERENCES Categories(CategoryName))""")

#Population of the tables from HTTP content
for element in data:
    for entry in element["products"]:
        #Check of the presence of critical keys/columns
        if ("categories" in entry.keys() and "product_name" in entry.keys() and "nutrition_grade_fr" in entry.keys()):
            if (entry["categories"] == ''):
                pass
                #print("cette cat est vide!")
            else:
                entry_split = entry["categories"].split(',')
                c.execute("""INSERT IGNORE INTO Categories (CategoryName) VALUES (%s)""", (entry_split[0],))
                c.execute("""INSERT IGNORE INTO Products (ProductName,CategoryName,Grade) VALUES (%s,%s,%s)""", (entry["product_name"],entry_split[0],entry["nutrition_grade_fr"],))
                print("Ce produit est ajouté :", entry["product_name"])
                #Import of location of the products, if it exists
                if ("stores" in entry.keys() and "product_name" in entry.keys()):
                    c.execute("""INSERT IGNORE INTO Products (Places,Stores) VALUES (%s,%s)""", (entry["purchase_places"],entry["stores"],))                
        else:
            print("Keys pas bonnes!!")


db.commit()
