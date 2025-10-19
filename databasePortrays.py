import sqlite3

def createTable():
    con = sqlite3.connect("../data/portrays.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS portrays(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    count INTEGER DEFAULT 0
    )"""

    cur.execute(sql)
    con.commit()
    con.close()

createTable()

def addPortrait(user_id, name):
    con = sqlite3.connect("../data/portrays.sqlite")
    cur = con.cursor()

    sql = "INSERT OR IGNORE INTO portrays(user_id, name) VALUES(?, ?)"

    # if getCount(user_id, name) == 0:
    cur.execute(sql, (user_id, name,))
    con.commit()
    con.close()


def getCount(user_id, name):
    con = sqlite3.connect("../data/portrays.sqlite")
    cur = con.cursor()

    sql = "SELECT count FROM portrays WHERE user_id = ? AND name = ?"

    cur.execute(sql, (user_id, name,))
    count = cur.fetchone()
    con.commit()
    con.close()
    return count[0] if count != None else 0

def updCount(user_id, name):
    con = sqlite3.connect("../data/portrays.sqlite")
    cur = con.cursor()
    count = getCount(user_id, name)

    sql = f"UPDATE portrays SET count = {count+1} WHERE user_id = ? AND name = ?"

    cur.execute(sql, (user_id, name,))
    con.commit()
    con.close()
