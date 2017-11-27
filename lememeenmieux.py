import MySQLdb
import json

"""

"""


#Connection to openfood db (The password will be stored in another file later !!)
db=MySQLdb.connect(user="root",passwd="ocsql",db="openfood")

c=db.cursor()
print("Le même en mieux : faites vous plaisir tout en mangeant mieux.")
print("Faites votre choix:")
print("1) Rechercher une catégorie")
print("2) Afficher les recherches sauvegardées")
#c.execute("""SELECT (id,CategoryName) FROM Categories""")

db.commit()
