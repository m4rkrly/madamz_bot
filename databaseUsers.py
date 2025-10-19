import sqlite3

class RegistrationError(BaseException): pass

def createUsers():
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY,
            username TEXT,
            isAdmin BOOLEAN DEFAULT False,
            current_pulls INTEGER DEFAULT 0,
            all_pulls INTEGER DEFAULT 0,
            gurantee INTEGER DEFAULT 0,
            six_times INTEGER DEFAULT 0,
            six_wins INTEGER DEFAULT 0,
            six_guranteed INTEGER DEFAULT 0
            )
            """
    
    cur.execute(sql)
    con.commit()
    con.close()

createUsers()

# ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В ТАБЛИЦУ (ID и его никнейм)
def addUser(id, username):
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = "INSERT OR IGNORE INTO users(id, username) VALUES(?, ?)"

    cur.execute(sql, (id, username))
    con.commit()
    con.close()

def isAdmin(id):
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = "SELECT isAdmin FROM users WHERE id = ?"

    cur.execute(sql, (id,))
    
    status = cur.fetchone()
    con.close()
    return status

def upgrade(id):
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = "UPDATE users SET isAdmin = 1 WHERE id = ?"

    cur.execute(sql, (id,))
    con.commit()
    con.close()

def downgrade(id):
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()
    
    sql = "UPDATE users SET isAdmin = 0 WHERE id = ?"

    cur.execute(sql, (id,))
    con.commit()
    con.close()

def getPulls(id):
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = "SELECT current_pulls, all_pulls, gurantee, six_times, six_wins, six_guranteed FROM users WHERE id = ?"

    cur.execute(sql, (id,))
    
    data = cur.fetchone()
    con.close()
    if data == None:
        raise RegistrationError
    else:
        return data

def updatePulls(args):
    # args - tuple(current_pulls, all_pulls, gurantee, six_times, six_wins, six_guranteed)
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()
    
    sql = "UPDATE users SET current_pulls = ?, all_pulls = ?, gurantee = ?, six_times = ?, six_wins = ?, six_guranteed = ? WHERE id = ?"

    cur.execute(sql, args)
    con.commit()
    con.close()