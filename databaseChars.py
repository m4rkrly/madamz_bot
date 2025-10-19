import sqlite3

class CharNameError(BaseException): pass
class RepeationError(BaseException): pass
class AmountError(BaseException): pass
class ArgumentTypeError(BaseException): pass

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
            resonance2 TEXT DEFAULT 0,
            resonance3 TEXT DEFAULT 0,
            smooches INTEGER DEFAULT 0
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
        if str(arg) == s[0] or (s[1] != None and any(str(arg) == i for i in s[1].split(', '))):
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
    if als == None: raise CharNameError
    return als

def addAliases(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(args[0])

    data = getAliases(args[0])[0]

    if data != None and data != "0":
        data = data.split(', ')
    else:
        data = list() 
    
    for i in args[1:]:
        if i not in data:
            data.append(i)
    
    data = ', '.join(data)

    sql = "UPDATE chars SET aliases = ? WHERE name = ?"
    
    cur.execute(sql, (data, name,))
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
            raise ArgumentTypeError
    else:
        raise CharNameError
    
    cur.execute(sql, (file_id, name))
    con.commit()
    con.close()

def addReson(args):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(args[0])

    if name != 0:
        if args[1] in ["1", "2", "3"]:
            sql = f"UPDATE chars SET resonance{args[1]} = ? WHERE name = ?"

            cur.execute(sql, (args[2], name,))
            con.commit()
            con.close()
        else:
            raise AmountError
    else:
        raise CharNameError 

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
        raise CharNameError 

# БЛОК №4 - ПОЛУЧЕНИЕ КАРТОЧЕК, РЕЗОНАНСОВ И ГАЙДА

def getPics(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)
    
    if name != 0:
        sql = "SELECT build, materials, resonance1, resonance2, resonance3 FROM chars WHERE name = ?"

        cur.execute(sql, (name,))
        pics = cur.fetchone()
        con.close()
        
        if pics[0] == "0":
            raise CharNameError
        else:
            return pics
    else:
        raise CharNameError

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
        raise CharNameError
    
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

def getAllBuilds():
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT name FROM chars WHERE build <> 0"

    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data

def getGuidedAliases():
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT aliases FROM chars WHERE guide <> 0"

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

    sql = "SELECT name, rarity, afflatus, dmgType, aliases, build, materials, guide, resonance1, resonance2, resonance3 FROM chars WHERE name = ? "

    cur.execute(sql, (name,))
    char = cur.fetchone()
    con.close()
    return char

# БЛОК №6 - РАЗВЛЕКАТЕЛЬНЫЕ ФУНКЦИИ

def smooch(arg):
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()
    name = getName(arg)

    if name != 0:
        cur.execute("SELECT smooches FROM chars WHERE name = ?", (name,))
        smooches = cur.fetchone()[0]

        sql = "UPDATE chars SET smooches = ? WHERE name = ?"

        cur.execute(sql, (smooches+1, name,))
        con.commit()
        con.close()
        return smooches+1    
    else:
        raise CharNameError
    
def getCharsbyStars(arg):
    # arg - rarity
    con = sqlite3.connect("../data/chars.sqlite")
    cur = con.cursor()

    sql = "SELECT name FROM chars WHERE rarity = ?"

    cur.execute(sql, arg)
    data = cur.fetchall()
    data = [i[0] for i in data]
    con.close()
    return 0 if data == None else data