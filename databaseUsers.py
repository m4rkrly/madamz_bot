import sqlite3

# СОЗДАНИЕ ТАБЛИЦЫ С СТОЛБЦАМИ ID, username, isAdmin
def createUsers():
    con = sqlite3.connect("../data/users.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY,
            username TEXT,
            isAdmin BOOLEAN DEFAULT False)
            """
    
    cur.execute(sql)
    con.commit()
    con.close()

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
