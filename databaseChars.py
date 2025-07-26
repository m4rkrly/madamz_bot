import sqlite3

def createTable():
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = """CREATE TABLE IF NOT EXISTS chars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rarity TEXT,
            afflatus TEXT,
            dmgType TEXT,
            aliases TEXT DEFAULT 0,
            build TEXT DEFAULT 0,
            materials TEXT DEFAULT 0,
            guide TEXT DEFAULT 0,
            resonance1 TEXT DEFAULT 0,
            resonance2 TEXT DEFAULT 0
            )"""
    
    cur.execute(sql)
    con.commit()
    con.close()

createTable()

# БЛОК №0 - САБФУНКЦИИ
def getName(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT name, aliases FROM chars"

    cur.execute(sql)
    data = cur.fetchall()

    for s in data:
        if arg in s[0] or arg in s[1]:
            return s[0]          
    else:
        return 0

def getTranslatedAlias(name):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT aliases FROM chars WHERE name = ?"

    cur.execute(sql, (name,))
    data = cur.fetchone()[0]
    con.close()

    data = data.split(', ')[0]
    return data

# БЛОК №1 - ПЕРВИЧНОЕ ДОБАВЛЕНИЕ ПЕРСОНАЖЕЙ, РЕДАКТИРОВАНИЕ ОСНОВНОЙ ИНФОРМАЦИИ И УДАЛЕНИЕ

# ДОБАВИТЬ ПЕРСОНАЖА
def addChar(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = """INSERT OR IGNORE INTO chars(name, rarity, afflatus, dmgType) VALUES(?, ?, ?, ?)"""

    cur.execute(sql, args)
    con.commit()
    # con.close()    

# ОТРЕДАКТИРОВАТЬ ПЕРСОНАЖА
def editChar(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = """UPDATE chars SET name = ?, rarity = ?, afflatus = ?, dmgType = ? WHERE name = ?"""

    cur.execute(sql, args)
    con.commit()
    con.close()


# УДАЛИТЬ ПЕРСОНАЖА
def delChar(name):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "DELETE FROM chars WHERE name = ?"

    cur.execute(sql, (name,))
    con.commit()
    con.close()

# БЛОК №2 - РАБОТА С ПСЕВДОНИМАМИ (aliases)
def getAliases(name):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT aliases FROM chars WHERE name = ?"

    cur.execute(sql, (name,))
    als = cur.fetchone()
    con.close()
    return als

def addAliases(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    data = getAliases(args[0])[0]
    name = getName(args[0])

    sql = "UPDATE chars SET aliases = ? WHERE name = ?"
    
    if data != "0":
        updated = data + ', ' + args[1]
    else:
        updated = args[1]
    
    cur.execute(sql, (updated, name,))
    con.commit()
    con.close()

def delAliases(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)

    sql = "UPDATE chars SET aliases = 0 WHERE name = ?"

    cur.execute(sql, (name,))
    con.commit()
    con.close()

# БЛОК №3 - ДОБАВЛЕНИЕ И ВЫВОД КАРТОЧЕК С РЕЗОНАНСАМИ (build, materials)

def addCard(arg, type, file_id):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)

    if name != 0:
        if type in ('build', 'b', 'билд', 'б'):
            sql = "UPDATE chars SET build = ? WHERE name = ?"
        elif type in ('materials', 'm', 'материалы', 'м'):
            sql = "UPDATE chars SET materials = ? WHERE name = ?"
        else:
            raise Exception
    else:
        raise NameError
    
    cur.execute(sql, (file_id, name))
    con.commit()
    con.close()

def addReson(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(args[0])

    if name != 0:
        if args[1] in ["1", "2"]:
            sql = f"UPDATE chars SET resonance{args[1]} = ? WHERE name = ?"

            cur.execute(sql, (args[2], name,))
            con.commit()
            con.close()
        else:
            raise Exception
    else:
        raise NameError 

def addGuide(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(args[0])

    if name != 0:    
        sql = f"UPDATE chars SET guide = ? WHERE name = ?"

        cur.execute(sql, (args[1], name,))
        con.commit()
        con.close()
    else:
        raise NameError 

# БЛОК №4 - ПОЛУЧЕНИЕ КАРТОЧЕК, РЕЗОНАНСОВ И ГАЙДА

def getPics(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)
    
    if name != 0:
        sql = "SELECT build, materials, resonance1, resonance2 FROM chars WHERE name = ?"

        cur.execute(sql, (name,))
        pics = cur.fetchone()
        con.close()
        
        if pics[0] == "0":
            raise NameError
        else:
            return pics
    else:
        raise NameError

def getGuide(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)
    
    if name != 0:
        sql = "SELECT guide FROM chars WHERE name = ?"

        cur.execute(sql, (name,))
        guide = cur.fetchone()
        con.close()
        return guide
    else:
        raise NameError
    
# БЛОК №5 - ФУНКЦИИ НАВИГАЦИИ

# ПОЛУЧИТЬ СПИСОК ИМЁН ВСЕХ ПЕРСОНАЖЕЙ
def getNames():
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT name FROM chars"

    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def getBuildableAliases():
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT aliases FROM chars WHERE build <> 0"

    cur.execute(sql)
    data = cur.fetchall()
    data = [(i[0].split(', '))[0] for i in data] # нужно подумать как это улучшить
    con.close()
    return data

# ПОЛУЧИТЬ ПЕРСОНАЖА
def getChar(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)

    sql = "SELECT name, rarity, afflatus, dmgType, aliases, build, materials, guide, resonance1, resonance2 FROM chars WHERE name = ? "

    cur.execute(sql, (name,))
    char = cur.fetchone()
    con.close()
    return char

# БЛОК №6 - РАЗВЛЕКАТЕЛЬНЫЕ ФУНКЦИИ

def smooch(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)

    cur.execute("SELECT smooches FROM chars WHERE name = ?", (name,))
    smooches = cur.fetchone()[0]

    sql = "UPDATE chars SET smooches = ? WHERE name = ?"

    cur.execute(sql, (smooches+1, name,))
    con.commit()
    con.close()
    return smooches+1    
