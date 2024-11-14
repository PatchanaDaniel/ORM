import sqlite3 as sq
def squery(arg,s):
    chn=''
    c=0
    for i in arg:
        v= f" '{arg[i]}'" if type(arg[i])==str else arg[i]
        chn= chn+f' {i} = {v} ' if c==0 else chn+ f' {s} {i} = {v} ' 
        c+=1
    return chn
class SqlBase:
    def __init__(self) -> None:
        pass
    con=sq.connect('mabase.db')
    cur=con.cursor()
    @classmethod
    def getVarName(cls):
        return   [ name+ f' {cls.__dict__[name] } ' for name in cls.__dict__ if  cls.__dict__[name] in ['TEXT','INTEGER','REAL']]
    @classmethod
    def run(cls):

        try:   
            l=cls.getVarName()
            chn=''
            for i in range(len(l)) :
                if i==len(l)-1:
                    chn+=l[i]+ '  )'
                    break
                chn+=l[i]+ '  ,'
            
            cls.cur.execute(f'''  
    CREATE TABLE IF NOT EXISTS {cls.__name__}(
    id INTEGER PRIMARY KEY AUTOINCREMENT , {chn}
    '''
    
    )   
        except:
            print(f"Erreur lors de la création de la table{cls.__name__} ")
    
    @classmethod
    def add(cls,**kwargs):

        try:
            col=''
            for i in kwargs:
                col+= " "+i+' ,'
            lgn=''
            
            for i in kwargs:
                v=kwargs[i]
                v=str(v)
                if not v.isdecimal():
                    v=f"'{v}'"
                lgn+=" "+v+' ,'
            
            cls.cur.execute(f''' INSERT INTO {cls.__name__} ( {col[:len(col)-1]} )
    VALUES
    ( {lgn[:len(lgn)-1]} ) 
    ''')
            cls.con.commit()
        except :
           print("Erreur lors de l'ajout des données ")
    @classmethod
    def all(cls,):
        res=cls.cur.execute(f''' SELECT * FROM {cls.__name__} 
    ''')
        return res.fetchall()

    @classmethod
    def filter(cls,**kwargs):
        try:
            res=cls.cur.execute(f''' SELECT * FROM {cls.__name__} WHERE { squery(kwargs,'and') };
        ''')
            return res.fetchall()
        except:
            print("Erreur lors de la récupération des donées")
            return []
    @classmethod
    def get(cls,**kwargs):
        try:
            res=cls.cur.execute(f''' SELECT * FROM {cls.__name__} WHERE { squery(kwargs,'and') };
        ''')
            return res.fetchone()
        except:
            print("Erreur lors de la récupération des donées")
            return []
    @classmethod
    def update(cls,condition:dict,**kwargs):
        try:
            cls.cur.execute(f"""
        UPDATE {cls.__name__}  SET {squery(kwargs,',')} WHERE {squery(condition,'and')};
        """) 
            cls.con.commit() 
        except:
             print(f"Erreur lors de la mise à jour du jour du champ id {id}")
    @classmethod
    def delete(cls,**kwargs):

        try:
            cls.cur.execute(f"""
    DELETE   FROM {cls.__name__} WHERE {squery(kwargs,'and')}
    """) 
            cls.con.commit()
        except:
            print(f"Erreur lors de la suppression du champ id={id}")

    @classmethod
    def delete_all(cls):

        try:
            cls.cur.execute(f"""
    DELETE   FROM {cls.__name__} 
    """) 
            cls.con.commit()
        except:
            print(f"Erreur lors de la suppression des  champs ")


        

IntField= 'INTEGER'
FloatField='REAL'
StringField='TEXT'

