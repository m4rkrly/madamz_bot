import sqlite3
import databaseChars as dbC

def createTable():
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS kits(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    kit TEXT,
    msgId INT DEFAULT 0, 
    type TEXT
    )"""

    cur.execute(sql)
    con.commit()
    con.close()

createTable()

# ДЛЯ РУЧНОГО ДОБАВЛЕНИЯ
def manualAddKit(args):
    # name, kit, msgId, type
    name = dbC.getName(args[0])
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()

    if name != 0:
        sql = "INSERT OR IGNORE INTO kits(name, kit, msgId, type) VALUES(?, ?, ?, ?)"

        cur.execute(sql, args)

        con.commit()
        con.close()
        return cur.lastrowid
    else:
        raise dbC.CharNameError

def manualDelKit(id):
    # id
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()

    sql = "DELETE FROM kits WHERE id = ?"

    cur.execute(sql, id)
    con.commit()
    con.close()

def addKit(args):
    #name, mainpostID, additSkills, additEuph"
    name = dbC.getName(args[0]) # [0] НЕ УБИРАТЬ
    rep = getKit((name)) # [0] НЕ УБИРАТЬ
    if rep != 0: raise dbC.RepeationError

    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    skills = 2 + args[2]
    euph = 1 + args[3]

    sql = "INSERT OR IGNORE INTO kits(name, kit, msgId, type) VALUES(?, ?, ?, ?)"

    if name != 0:    
        # Основной пост
        cur.execute(sql, (name, "mainpost", args[1], "a"))
        # Инсайт
        cur.execute(sql, (name, "insight", args[1]+1, "i"))
        # Навыки
        for n in range(1, skills+1):
            cur.execute(sql, (name, f"skill", (args[1]+1)+n, "s"))
        # Ультимейт
        cur.execute(sql, (name, "ultimate", (args[1]+skills+2), "u"))
        # Портреты
        cur.execute(sql, (name, "portrays", (args[1]+skills+3), "p"))
        # Эйфории
        for n in range(1, euph+1):
            cur.execute(sql, (name, 'euphoria', (args[1]+skills+3+n), "e"))
    else:
        raise dbC.CharNameError

    con.commit()
    con.close()

def delKit(arg):
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    name = dbC.getName(arg)

    if name != 0:
        sql = "DELETE FROM kits WHERE name = ?"

        cur.execute(sql, (name,))
        con.commit()
        con.close()
    else:
        raise dbC.CharNameError

def getKit(arg):
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    name = dbC.getName(arg)

    if name != 0:
        sql = "SELECT msgID, type FROM kits WHERE name = ?"

        cur.execute(sql, (name,))
        data = cur.fetchall()
        con.close()
        return data if data != [] else 0
    else:
        raise dbC.CharNameError

def getAllKits():
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    
    sql = "SELECT name FROM kits"

    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data