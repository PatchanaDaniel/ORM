```python
# ORM
#orm (Object-Relational Mapper) pour intéragir avec sqlite

from db_orm import SqlBase, StringField, IntField, FloatField

#creation de la table Eleve/ creation table Eleve

class  Eleve (SqlBase):

    nom=StringField
    classe=StringField
    age=IntField
    moyenne=FloatField

#Ajout d'élements



Eleve.add(nom='sam',
          classe='TleD',
          age='16',
          moyenne='18')
          

Eleve.add(nom='theo',
          classe='TleC',
          age='17',
          moyenne='16')

#Mise à jour 

Eleve.update(condition={'nom':'theo'},
  moyenne=15.5           

)
#recupérer tous les champs

stu_all=Eleve.all()

#recuperer les champs repondant à un critére

stu_filtered =Eleve.filter(age=16)

#recupérer un champ

stu_one = Eleve.get(nom='theo')

#Suppresion d'un element

Eleve.delete( nom='theo')

#Suppresion de tous les données de la table

Eleve.delete_all()

```