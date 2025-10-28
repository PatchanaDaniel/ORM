import sqlite3 as sq


def structured_conditions(arg, operator):
    """Fonction pour structurer les conditions d'une requête SQL c'est à dire ce qui vient après le WHERE \n
    Function to structure the conditions of an SQL query, that is, what comes after the WHERE"""
    cols_with_lines = ''
    counter = 0
    for col in arg:
        line = f" '{arg[col]}'" if type(arg[col]) == str else arg[col]
        cols_with_lines = cols_with_lines + f' {col} = {line} ' if counter == 0 else cols_with_lines + f' {operator} {col} = {line} '
        counter += 1
    return cols_with_lines


class SqlBase():
    """Classe de base pour la création des tables et la gestion des données \n
    Base class for table creation and data management\n
        Exemple / Example :
    class  Eleve(SqlBase):
    nom=StringField 
    classe=StringField
    age=IntField
    moyenne=FloatField

    le nom de la table sera le nom de la classe (Eleve) et les champs seront nom,classe,age et moyenne \n
    the table name will be the class name (Eleve) and the fields will be nom, classe, age, and moyenne
    Eleve.run()  # création de la table / table creation
    """

    def __init__(self) -> None:
        pass

    connection = sq.connect('mybase.db')
    cursor = connection.cursor()

    @classmethod
    def get_col_with_type(cls):
        return [
            col + f' {cls.__dict__[col] } ' for col in cls.__dict__
            if cls.__dict__[col] in ['TEXT', 'INTEGER', 'REAL']
        ]

    @classmethod
    def run(cls):

        try:
            cols_with_types_list = cls.get_col_with_type()
            cols_with_types_list_str = ''
            for i in range(len(cols_with_types_list)):
                if i == len(cols_with_types_list) - 1:
                    cols_with_types_list_str += cols_with_types_list[i] + '  )'
                    break
                cols_with_types_list_str += cols_with_types_list[i] + '  ,'

            cls.cursor.execute(f""" 
    CREATE TABLE IF NOT EXISTS {cls.__name__}(
    id INTEGER PRIMARY KEY AUTOINCREMENT , {cols_with_types_list_str}
    """)
        except Exception as e:
            print(f"""Erreur lors de la création de la table {cls.__name__} \n
    Error while creating the table {cls.__name__}
    Détails de l'erreur : {e}
                  """)

    @classmethod
    def add(cls, **kwargs):
        """Méthode pour ajouter des données dans la table \n
        Method to add data to the table \n
        Exemple / Example :
        Eleve.add(nom='sam',
          classe='TleD',
          age='16',
          moyenne='18')"""

        try:
            cols_formated = ''
            lines_formated = ''
            for col in kwargs:
                cols_formated += " " + col + ' ,'

                line = kwargs[col]
                line = str(line)
                if not line.isdecimal():
                    line = f"'{line}'"
                lines_formated += " " + line + ' ,'

            cls.cursor.execute(
                f''' INSERT INTO {cls.__name__} ( {cols_formated[:len(cols_formated)-1]} )
    VALUES
    ( {lines_formated[:len(lines_formated)-1]} ) 
    ''')
            cls.connection.commit()
        except:
            print("""Erreur lors de l'ajout des données \n
    Error while adding data""")

    @classmethod
    def all(cls, ):
        """Méthode pour récupérer toutes les données de la table \n
        Method to get all data from the table \n
        Exemple / Example :
        students_all=Eleve.all()  #récupérer tous les champs / get all fields"""
        res = cls.cursor.execute(f""" SELECT * FROM {cls.__name__} 
    """)
        return res.fetchall()

    @classmethod
    def filter(cls, **kwargs):
        """Méthode pour filtrer les données de la table \n
        Method to filter data from the table 
        Exemple / Example :
        students_filtered=Eleve.filter(age=16,classe='TleD')  #"""
        try:
            res = cls.cursor.execute(
                f""" SELECT * FROM {cls.__name__} WHERE { structured_conditions(kwargs,'and') };
        """)
            return res.fetchall()
        except:
            print("""Erreur lors de la récupération des donées \n
    Error while retrieving data""")
            return []

    @classmethod
    def get(cls, **kwargs):
        """Méthode pour récupérer un seul élément de la table \n
        Method to get a single item from the table \n
        Exemple / Example :
        student=Eleve.get(nom='theo')  #récupérer un champ / get one field"""
        try:
            res = cls.cursor.execute(
                f""" SELECT * FROM {cls.__name__} WHERE { structured_conditions(kwargs,'and') };
        """)
            return res.fetchone()
        except:
            print("""Erreur lors de la récupération des donées \n
    Error while retrieving data""")
            return []

    @classmethod
    def update(cls, condition: dict, **kwargs):
        """Méthode pour mettre à jour un élément de la table \n
        Method to update an item in the table
        Exemple / Example :
        Eleve.update(condition={'nom':'theo'},
          moyenne=15.5           
        )"""
        try:
            cls.cursor.execute(f"""
        UPDATE {cls.__name__}  SET {structured_conditions(kwargs,',')} WHERE {structured_conditions(condition,'and')};
        """)
            cls.connection.commit()
        except:
            print(f"""Erreur lors de la mise à jour du jour du champ id {id} \n
    Error while updating the field id {id}""")

    @classmethod
    def delete(cls, **kwargs):
        """Méthode pour supprimer un élément de la table \n
        Method to delete an item from the table 
        Exemple / Example :
        Eleve.delete( nom='theo')  #supprimer un champ / delete one field"""
        try:
            cls.cursor.execute(f"""
    DELETE   FROM {cls.__name__} WHERE {structured_conditions(kwargs,'and')}
    """)
            cls.connection.commit()
        except:
            print(f"""Erreur lors de la suppression du champ id={id} \n
    Error while deleting the field id={id}""")

    @classmethod
    def delete_all(cls):
        """Méthode pour supprimer tous les éléments de la table \n
        Method to delete all items from the table
        Exemple / Example :
        Eleve.delete_all()  #supprimer tous les champs / delete all fields"""
        try:
            cls.cursor.execute(f"""
    DELETE   FROM {cls.__name__} 
    """)
            cls.connection.commit()
        except:
            print("""Erreur lors de la suppression des  champs \n
    Error while deleting the fields""")


IntField = 'INTEGER'  # Champ entier/ Integer field
FloatField = 'REAL'  # Champ flottant/ Float field
StringField = 'TEXT'  # Champ texte/ Text field
