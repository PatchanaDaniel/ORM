import sqlite3 as sq


class Meta(type):

    def __getattribute__(cls, name):
        attr = super().__getattribute__(name)
        # Intercepter toutes les méthodes sauf celles qui commencent par __ et run
        except_func = ("run", "__class__", "__dict__", "__module__",
                       f"_SqlBase__get_col_with_type",
                       "_SqlBase__structured_conditions", "connection",
                       "cursor")
        if callable(attr) and name not in except_func:

            def new_func(*args, **kwargs):
                # Appel direct de run sans repasser par le wrapper
                super(Meta, cls).__getattribute__("run")()
                return attr(*args, **kwargs)

            return new_func
        return attr


# Aucun objet n’est nécessaire


class SqlBase(metaclass=Meta):
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
    def __get_col_with_type(cls):
        return [
            col + f' {cls.__dict__[col] } ' for col in cls.__dict__
            if cls.__dict__[col] in ['TEXT', 'INTEGER', 'REAL']
        ]

    @staticmethod
    def __structured_conditions(arg, operator):
        """Fonction pour structurer les conditions d'une requête SQL c'est à dire ce qui vient après le WHERE \n
        Function to structure the conditions of an SQL query, that is, what comes after the WHERE"""
        cols_with_lines = ''
        counter = 0
        for col in arg:
            line = f" '{arg[col]}'" if type(arg[col]) == str else arg[col]
            cols_with_lines = cols_with_lines + f' {col} = {line} ' if counter == 0 else cols_with_lines + f' {operator} {col} = {line} '
            counter += 1
        return cols_with_lines

    @staticmethod
    def __exceptions_management(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except sq.DataError:
                print("Erreur de données \n Data error")
            except sq.OperationalError:
                print(
                    "Erreur avec les opérations de la base de données \n error with database operations"
                )
            except sq.IntegrityError:
                print(
                    "Erreur d'intégrité de la base de données \n Database integrity error"
                )
            except sq.InternalError:
                print(
                    "Erreur interne de la base de données SQLite\n Internal database error"
                )
            except sq.ProgrammingError:
                print(
                    "Erreur de connexion avec SQLite\n Connection error with SQLite"
                )
            except sq.DatabaseError:
                print(
                    "Erreur générale de la base de données SQLite\n General SQLite database error"
                )
            except sq.InterfaceError:
                print(
                    "Erreur d'interface avec le module sqlite3\n Interface error with the sqlite3 module"
                )
            except sq.Error as e:
                print(
                    f"Une erreur SQLite est survenue : {e}\n An SQLite error occurred: {e}"
                )
            except Exception as e:
                print(
                    f"Une erreur inattendue est survenue,probablement liée à la logique du module : {e}\n An unexpected error occurred, probably related to the module logic: {e}"
                )

        return wrapper

    @classmethod
    @__exceptions_management
    def run(cls):
        """Méthode pour demarrer les configurations de la table dans la base de données \n
        Method to start configuring the table in the database"""

        cols_with_types_list = cls.__get_col_with_type()
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

    @classmethod
    @__exceptions_management
    def add(cls, **kwargs):
        """Méthode pour ajouter des données dans la table \n
        Method to add data to the table \n
        Exemple / Example :
        Eleve.add(nom='sam',
          classe='TleD',
          age='16',
          moyenne='18')"""

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
            f""" INSERT INTO {cls.__name__} ( {cols_formated[:len(cols_formated)-1]} )
    VALUES
    ( {lines_formated[:len(lines_formated)-1]} ) 
    """)
        cls.connection.commit()

    @classmethod
    @__exceptions_management
    def all(cls, ):
        """Méthode pour récupérer toutes les données de la table \n
        Method to get all data from the table \n
        Exemple / Example :
        students_all=Eleve.all()  #récupérer tous les champs / get all fields"""
        res = cls.cursor.execute(f""" SELECT * FROM {cls.__name__} 
    """)
        return res.fetchall()

    @classmethod
    @__exceptions_management
    def filter(cls, **kwargs):
        """Méthode pour filtrer les données de la table \n
        Method to filter data from the table 
        Exemple / Example :
        students_filtered=Eleve.filter(age=16,classe='TleD')  #"""

        res = cls.cursor.execute(
            f""" SELECT * FROM {cls.__name__} WHERE { cls.__structured_conditions(kwargs,'and') };
        """)
        return res.fetchall()

    @classmethod
    @__exceptions_management
    def get(cls, **kwargs):
        """Méthode pour récupérer un seul élément de la table \n
        Method to get a single item from the table \n
        Exemple / Example :
        student=Eleve.get(nom='theo')  #récupérer un champ / get one field"""

        res = cls.cursor.execute(
            f""" SELECT * FROM {cls.__name__} WHERE { cls.__structured_conditions(kwargs,'and') };
        """)
        return res.fetchone()

    @classmethod
    @__exceptions_management
    def update(cls, condition: dict, **kwargs):
        """Méthode pour mettre à jour un élément de la table \n
        Method to update an item in the table
        Exemple / Example :
        Eleve.update(condition={'nom':'theo'},
          moyenne=15.5           
        )"""

        cls.cursor.execute(f"""
        UPDATE {cls.__name__}  SET {cls.__structured_conditions(kwargs,',')} WHERE {cls.__structured_conditions(condition,'and')};
        """)
        cls.connection.commit()

    @classmethod
    @__exceptions_management
    def delete(cls, **kwargs):
        """Méthode pour supprimer un élément de la table \n
        Method to delete an item from the table 
        Exemple / Example :
        Eleve.delete( nom='theo')  #supprimer un champ / delete one field"""

        cls.cursor.execute(f"""
    DELETE   FROM {cls.__name__} WHERE {cls.__structured_conditions(kwargs,'and')}
    """)
        cls.connection.commit()

    @classmethod
    @__exceptions_management
    def delete_all(cls):
        """Méthode pour supprimer tous les éléments de la table \n
        Method to delete all items from the table
        Exemple / Example :
        Eleve.delete_all()  #supprimer tous les champs / delete all fields"""

        cls.cursor.execute(f"""
    DELETE   FROM {cls.__name__} 
    """)
        cls.connection.commit()


IntField = 'INTEGER'  # Champ entier/ Integer field
FloatField = 'REAL'  # Champ flottant/ Float field
StringField = 'TEXT'  # Champ texte/ Text field
