import sqlite3
import databaseChars

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

def addKit(args):
    #name, mainpostID, additSkills, additEuph"
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    name = databaseChars.getName(args[0])
    skills = 2 + args[2]
    euph = 1 + args[3]

    sql = "INSERT OR IGNORE INTO kits(name, kit, msgID, type) VALUES(?, ?, ?, ?)"

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
        raise NameError

    con.commit()
    con.close()

def delKit(arg):
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    name = databaseChars.getName(arg[0])

    if name != 0:
        sql = "DELETE FROM kits WHERE name = ?"

        cur.execute(sql, (name,))
        con.commit()
        con.close()
    else:
        raise NameError

def getKit(arg):
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    name = databaseChars.getName(arg[0])

    if name != 0:
        sql = "SELECT msgID, type FROM kits WHERE name = ?"

        cur.execute(sql, (name,))
        data = cur.fetchall()
        con.close()
        return data
    else:
        raise NameError
    
def getAllKits():
    con = sqlite3.connect("../data/kits.sqlite")
    cur = con.cursor()
    
    sql = "SELECT name FROM kits"

    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data
