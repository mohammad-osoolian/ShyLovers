import psycopg2
import os

def config(filename='database.ini', section='postgresql'):
    db = {}
    db['host'] = os.getenv('HOST')
    db['database'] = os.getenv('DATABASE')
    db['user'] = os.getenv('USER')
    db['password'] = os.getenv('PASSWORD')
    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error


class BotUserDBController:
    def __init__(self, conn):
        self.conn = conn
    
    def read(self, id):
        with self.conn , self.conn.cursor() as cur:
            cur.execute('SELECT * FROM BOTUSER WHERE id = %s', (id,))
            result = cur.fetchone()
        return result
    
    def readall(self):
        with self.conn, self.conn.cursor() as cur:
            cur.execute('SELECT * FROM BOTUSER')
            result = cur.fetchall()
        return result

    def update(self, id, st, csh, lng):
        with self.conn, self.conn.cursor() as cur:
            cur.execute('UPDATE BOTUSER SET st = %s, csh = %s, lng = %s WHERE id = %s', (st, csh, lng, id))
        return
    
    def delete(self, id):
        with self.conn, self.conn.cursor() as cur:
            cur.execute('DELETE FROM BOTUSER WHERE id = %s', (id,))
        return
    
    def create(self, id, st, csh, lng):
        with self.conn, self.conn.cursor() as cur:
            cur.execute('INSERT INTO BOTUSER VALUES (%s, %s, %s, %s)', (id, st, csh, lng))
        return


class BotUser:
    ctrl = None
    STATUSES = (0,1,2,3,4)
    LANGUAGES = ('en','far')

    def __init__(self, id:int):
        if not BotUser.isuser(id):
            raise Exception("user with this id doesn't exist")
        usr = self.ctrl.read(id)
        self._id = id
        self._st = usr[1]
        self._csh = usr[2]
        self._lng = usr[3]
    
    def updatedb(self):
        self.ctrl.update(self.id, self.st, self.csh, self.lng)

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, v):
        raise Exception('id cannot be set.')
    
    @property
    def st(self):
        return self._st
    @st.setter
    def st(self, v):
        if v not in self.STATUSES:
            raise Exception('status is not valid.')
        self._st = v
        self.updatedb()
        
    @property
    def csh(self):
        return self._csh
    @csh.setter
    def csh(self, v):
        if v == self.id:
            raise Exception('csh canot be equal to id.')
        self._csh = v
        self.updatedb()
    
    @property
    def lng(self):
        return self._lng
    @lng.setter
    def lng(self, v):
        if v not in self.LANGUAGES:
            raise Exception('language is not valid.')
        self._lng = v
        self.updatedb()

    @classmethod
    def isuser(cls, id):
        users = cls.ctrl.readall()
        return id in [user[0] for user in users]
    
    @classmethod
    def newuser(cls, id, st=0, csh=None, lng='en'):
        if cls.isuser(id):
            raise Exception('duplicate id')
        cls.ctrl.create(id, st, csh, lng)
        usr = BotUser(id)
        return usr
    
    def ismatched(self):
        if BotUser.isuser(self.csh):
            crush = BotUser(self.csh)
            if (self.csh == crush.id and crush.csh == self.id 
                and self.st == 4 and crush.st == 4):
                return True
        return False
    
    def clear(self):
        self.st = 0
        self.csh = None
        usr = BotUser(self.id)
        assert usr.csh == None and usr.st == 0

