import hashlib
from  tkinter import messagebox
import sqlite3 as sq


from getpass import getpass
from hashlib import *

# conn = sq.connect("Ma_base.dbs")
# c = conn.cursor()
# # c.execute("DROP TABLE User")
# c.execute("""create table if not exists User(
#     id integer primary key autoincrement,
#     num_cart text,
#     nom text,
#     prenom text,
#     pseudo text,
#     email text,
#     password text,
#     certPath text,
#     keyPath text,
#     is_connected boolean default 0
#     )""")
# conn.commit()
# conn.close()
def db_conn():
    try:
        conn = sq.connect("chat_db.dbs")
        c = conn.cursor()
    except:
        messagebox.showerror('Error','cant connect to database ')
        return

    c.execute("""create table if not exists User(
    id integer primary key autoincrement,
    email text,
    username text,
    password text
    )""")
    return conn, c



def signUp(username, email, password):
    conn, c = db_conn()
    if getUserByUsername(username)!=None:
        messagebox.showerror('Error','username already exists ')
    else:
        c.execute("""insert into User(email,username,password) values(?,?,?)""",
                  (email, username, hashlib.sha256(password.encode()).hexdigest()))
        c.execute("""select * from User""")
        items = c.fetchall()
        for item in items:
            print(item)

        conn.commit()
        conn.close()






def signIn(username, pwd):
    conn, c = db_conn()
    c.execute("""select * from User where username=? and password=?""",(username,hashlib.sha256(pwd.encode()).hexdigest()))
    items = c.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()
    if items:
        return items[0]
    else:
      return None

def getUserById(id):
    conn, c = db_conn()
    c.execute("""select * from User where id=?""", (id,))
    item = c.fetchone()

    print(item)
    conn.commit()
    conn.close()
    if item:
        return User(*item)
    else:
        return None
def getUserByUsername(email):
    conn, c = db_conn()
    c.execute("""select * from User where username=?""", (email,))
    item = c.fetchone()

    print(item)
    conn.commit()
    conn.close()
    if item:

        return item
    else:
        return None
def connecter(id):
    conn, c = db_conn()
    c.execute("""update User set is_connected=1  where id=?""", (id,))
    conn.commit()
    conn.close()
def deconnecter(id):
    conn, c = db_conn()
    c.execute("""update User set is_connected=0  where id=?""", (id,))
    conn.commit()
    conn.close()

def getConnectedUsers():
    conn, c = db_conn()
    c.execute("""select * from User where is_connected=1""", )
    items = c.fetchall()


    conn.commit()
    conn.close()

    return items


# signUp("1245", "safouuuuuu", "med", "saff", "safa1@gmail.com", "****",'hgjh','jhvjmb')
# connecter(1)
# nom=getUserById(1)
# w=signIn("safa1@gmail.com", "****")
# nom=getUserById(w)
# print(type(nom))
#getUserByEmail('emna@gmail.com')
# signUp('789','pirate','ben pirate','piratouu','pirate@gmail.com','000','build/pirate.cert','build/pirate.key')