from telebot import *
from telebot.types import *
import databaseUsers as dbU
import databaseChars as dbC
import databaseKits as dbK
import databasePortrays as dbP
from random import randint, choice

# КОНСТАНТЫ И ОБРАЩЕНИЯ К ДРУГИМ ФАЙЛАМ
TOKEN = "6721429873:AAE_VKvIN0AXog4HOdeWaSzfIZc3gZsG-a8"
PRYDWEN = 'https://www.prydwen.gg/re1999/characters/'
OWNERS = [1099300504, 6106161997] # здесь ввести ID того, кто будет ответственным за бота. у него будут неснимаемые права админа.
PODVAL = [-1001914465003, 190466]
LIBRARY = "@conundrum_library"
LIBRARYLINK = "https://t.me/conundrum_library/"
LIMBS = ["жопа", "попа", "жёпа", "голова", "лобик", "лоб", "носик", "макушка", "щёчка", "щечка", "грудь", "бубсы", "бубисы", "пятки", "ноги"]
KITTYPES = [("mainpost", "insight", "skill", "ultimate", "portrays", "euphoria", "assassin"), ("a", "i", "s", "u", "p", "e", "c")]

# КАСТОМНЫЕ ОШИБКИ
class LackArgsError(BaseException): pass

bot = TeleBot(TOKEN)

# ----------------- САБФУНКЦИИ ------------------------------------------------------------------------------------------

# (АДМИН) ПРОВЕРКА ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ АДМИНИСТРАТОРОМ/ВЛАДЕЛЬЦЕМ
def isAdmin(message):
    if dbU.isAdmin(message.from_user.id) == (1,) or message.from_user.id in OWNERS:
        return True
    else: 
        return False

# (БД) ПОЛУЧЕНИЕ АРГУМЕНТОВ ДЛЯ ЗАНЕСЕНИЯ В БД
def getArgs(raw, quantity = -1, minimize = -2):
    try:
        raw = raw[raw.index(" ") + 1:]
        if raw == [] or (quantity != -1 and len(raw.split(', ')) != quantity): raise LackArgsError
        if minimize == -2: 
            raw = tuple([a.lower() for a in raw.split(', ')])
        elif minimize == -1:
            raw = tuple(a for a in raw.split(', '))
        else:
            raw = raw.split(', ')
            fin = [raw[i] for i in range(len(raw)) if i != minimize]
            fin.insert(minimize, raw[minimize].lower())
            raw, fin = tuple(fin), []
        return raw
    except:
        raise LackArgsError

def makePretty(alias):
    args = dbC.getName(alias)
    alias = dbC.getAliases(args)[0].split(', ')[0]
    alias = alias[0].upper() + alias[1:]

    try:
        alias = alias[:alias.index(' ')+1:] + alias[alias.index(' ')+1].upper() + alias[alias.index(' ')+2:]
    except:
        pass
    return alias

# ----------------- ОБЩИЕ ПОЛЬЗОВАТЕЛЬСКИЕ КОМАНДЫ И СВЯЗАННЫЕ С НИМИ ФУНКЦИИ ------------------------------------------------------------------------------------------
    
# ПРИВЕТСТВИЕ  
@bot.message_handler(commands = ["start"])
def start(message):
    text = "<b>Приветствую!</b>\nВы можете ознакомиться с доступными командами через команду /help"

    bot.send_message(message.chat.id, text, parse_mode = "HTML")

# РЕГИСТРАЦИЯ
@bot.message_handler(commands = ["reg"])
def reg(message):
    try: 
        dbU.addUser(message.from_user.id, message.from_user.username)
        
        bot.reply_to(message, "Вы были успешно зарегистрированы!")
    except:
        bot.reply_to(message, "Не удалось зарегистрировать")

# ОБЩАЯ ПОМОЩЬ
@bot.message_handler(commands = ["help"])
def help(message):
    text = [
    """
<b>ПОЛЬЗОВАТЕЛЬСКИЕ КОМАНДЫ</b>
<i>Все аргументы в командах пишутся через запятую с пробелом!</i>
1. /reg - зарегистрироваться в боте (для /pull)
2. <code>/pull</code> [имя 6* персонажа] [(не обязательно) кол-во круток (до 10)] - покрутить баннер с персонажем (перед этим нужно использовать /reg) <b>(ТОЛЬКО В ТОПИКЕ ГАЧАРОЛЛ)</b>
3. /mypulls - узнать свою статистику по круткам 
4. <code>/smooch</code> [часть тела] [имя персонажа] - поцеловать персонажа (куда-либо) <b>НЕ ИСПОЛЬЗОВАТЬ ПОДОЗРИТЕЛЬНЫЕ ЧАСТИ ТЕЛА НА ДЕТЯХ, ЭТО НАКАЗУЕМО</b>
5. <code>/link</code> [<code>ru</code>, <code>cn</code>, <code>con</code>] - получить ссылку на канал: Фонд, Китайка, Конундрум
6. <code>/prydwen</code> [имя персонажа] - получить ссылку на персонажа на Prydwen
7. /buildhelp - получить список персонажей, имеющих карточки в <code>/build</code>
8. <code>/build</code> [имя персонажа] - получить карточки билда персонажа
9. /kithelp - получить список персонажей, имеющих <code>/kit</code>
10. <code>/kit</code> [имя персонажа], [<code>i</code> - инсайт, <code>s</code> - навыки, <code>p</code> - портреты, <code>u</code> - ультимейт, <code>e</code> - эйфория, <code>c</code> - способности ассасина (только для персонажей коллаборации)] - получить перевод скиллсета персонажа или отдельные его части
11. /guidehelp - получить список персонажей, имеющих <code>/guide</code>
12. <code>/guide</code> [имя персонажа] - получить гайд на персонажа
    """
    ]
    bot.reply_to(message, text, parse_mode = 'HTML')

# ССЫЛКИ НА КАНАЛЫ
# тут потом можно добавить кнопки
@bot.message_handler(commands = ["link"])
def links(message):
    channels = {
        'ru':'https://t.me/stpf_info',
        'cn':'https://t.me/Reverse1999_Cn',
        'con':'https://t.me/re99_conundrum'
        }
    arg = getArgs(message.text)[0]

    if arg in channels:
        bot.reply_to(message, channels.get(f'{arg}'))
    else:
        bot.reply_to(message, "Пожалуйста, уточните на какой канал вы хотите получить ссылку.\n1. ru - Фонд Святого Павлова\n2. cn - Канал по китайской версии\n3. con -  Conundrum\nПример: /link ru")

# ССЫЛКА НА ПЕРСОНАЖА НА PRYDWEN
@bot.message_handler(commands = ["prydwen"])
def prydwen(message):
    arg = dbC.getName(getArgs(message.text)[0])
    if arg == 0: bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище персонажа)") 
    chars = [l[0] for l in dbC.getNames()] 
    if arg in chars:
        bot.reply_to(message, PRYDWEN + arg)
    else:
        bot.reply_to(message, "К сожалению, нет либо этого персонажа, либо такой вариации его имени")

@bot.message_handler(commands = ["guidehelp"])
def guidehelp(message):
    try:
        data = dbC.getGuidedAliases()
        data = [f'<code>{a}</code>' for a in data]
        text = ", ".join(data)

        bot.reply_to(message, f"<b>Персонажи, доступные для команды <code>/guide</code></b>\n{text}", parse_mode = "HTML")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

# ВЫВОД ГАЙДА ДЛЯ ПЕРСОНАЖА (/guide)
@bot.message_handler(commands = ["guide"])
def guide(message):
    try:
        arg = getArgs(message.text)[0]
        data = dbC.getGuide(arg)
        if data[0] == "0": raise dbC.CharNameError
        bot.reply_to(message, f'{data[0]}')
    except LackArgsError:
        bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище персонажа)")
    except dbC.CharNameError:
        bot.reply_to(message, "К сожалению, нет либо гайда этого персонажа, либо такой вариации его имени\nВыберите персонажа исходя из списка в /guidehelp")
    except Exception as exc:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
        bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}")

# ВЫВОД КАРТОЧКИ ПРОКАЧКИ И МАТЕРИАЛОВ ДЛЯ ПЕРСОНАЖА (/build)
@bot.message_handler(commands = ['build'])
def build(message):
    try:
        arg = getArgs(message.text)[0]
        data = dbC.getPics(arg)
        text = str()
        if data[-3] != '0':
            text = f"<b>Коды резонансов</b>\n" + f"R1: <code>{data[-3]}</code>".replace("\n", "")
        if data[-2] != "0":
            text += "\n" + f"R2: <code>{data[-2]}</code>".replace("\n", "")
        if data[-1] != "0":
            text += "\n" + f"R3: <code>{data[-1]}</code>".replace("\n", "")    
        if data[1] == '0':
            pics = [InputMediaPhoto(data[0], caption = text, parse_mode="HTML")]
        else:
            pics = [InputMediaPhoto(data[0], caption = text, parse_mode="HTML"), InputMediaPhoto(data[1])]

        if message.chat.is_forum == True:
            bot.send_media_group(message.chat.id, pics, message_thread_id = message.message_thread_id)
        else:
            bot.send_media_group(message.chat.id, pics)

    except LackArgsError:
        bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище персонажа)")
    except dbC.CharNameError:
        bot.reply_to(message, "К сожалению, нет либо карточки этого персонажа, либо такой вариации его имени\nВоспользуйтесь /buildhelp для того, чтобы найти нужного персонажа")
    except Exception as exc:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
        bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}")

# ВЫВОД ВСЕХ ДОСТУПНЫХ ПЕРСОНАЖЕЙ ДЛЯ /build
@bot.message_handler(commands = ['buildhelp'])
def buildhelp(message):
    # try:
        data = dbC.getAllBuilds()
        data = [f'<code>{dbC.getTranslatedAlias(a[0])}</code>' for a in data]
        text = ", ".join(sorted(data))

        bot.reply_to(message, f"<b>Персонажи, доступные для команды <code>/build</code></b>\n{text}", parse_mode = "HTML")
    # except:
    #     bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

# ВЫВОД СКИЛЛСЕТОВ ПЕРСОНАЖЕЙ (/kit)
@bot.message_handler(commands = ['kit'])
def kit(message):
    try:
        args = getArgs(message.text)
        data = dbK.getKit(args[0])
        if data == 0: raise dbC.CharNameError

        if len(args) == 1:
            id = data[0]
            bot.forward_message(chat_id = message.chat.id, message_thread_id= message.message_thread_id, from_chat_id = f"{LIBRARY}", message_id = int(id[0]))
                
        elif len(args) == 2 and args[1] in ('i', 's', 'p', 'u', 'e', 'c'):
            for id in data:
                if id[1] == args[1] and message.chat.is_forum == True: bot.forward_message(chat_id = message.chat.id, message_thread_id= message.message_thread_id, from_chat_id = f"{LIBRARY}", message_id = int(id[0]))
                if id[1] == args[1] and message.chat.is_forum != True: bot.forward_message(chat_id = message.chat.id, from_chat_id = f"{LIBRARY}", message_id = int(id[0]))  
        else:
            bot.reply_to(message, "Неправильный ввод")
    except dbC.CharNameError:
        bot.reply_to(message, "К сожалению, нет либо скиллсета этого персонажа, либо такой вариации его имени\nВоспользуйтесь /kithelp для того, чтобы найти нужного персонажа")
    except Exception as exc:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
        bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}")

@bot.message_handler(commands = ['kithelp'])
def kitHelp(message):
    try:
        data = set([i[0] for i in dbK.getAllKits()])
        data = [f'<code>{dbC.getTranslatedAlias(j)}</code>' for j in data]
        data = ', '.join(sorted(data))
        
        bot.reply_to(message, f"<b>Список персонажей, доступных для <code>/kit</code>:</b>\n{data}", parse_mode = "HTML")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

# ----------------- КРУТКИ И РАЗВЛЕКАТЕЛЬНЫЕ ФУНКЦИИ --------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands = ['smooch'])
def smooch(message):
    try:
        args = getArgs(message.text)[0]
        add = str()
        if any(args.startswith(i+' ') for i in LIMBS):
            add = f" в {args[:args.index(' ')].lower()}"
            args = args[args.index(' ')+1:]
        smooches = dbC.smooch(args)
        alias = makePretty(args)
        text = f"Вы поцеловали {alias}{add}! Теперь на нём/ней {smooches} поцелуев"

        bot.reply_to(message, text)
    except dbC.CharNameError:
        bot.reply_to(message, "К сожалению, нет либо этого персонажа, либо такой вариации его имени")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

@bot.message_handler(commands = ["mypulls"])
def mypulls(message):
    data = dbU.getPulls(message.from_user.id)
    
    text = f"<b>Приветствую, {message.from_user.username if message.from_user.username != None else "Пользователь"}!</b>\n<i>Всего:</i> {data[1]}, <i>Откручено:</i> {data[0]}\nW/G/A = {data[4]}/{data[5]}/{data[3]}, <i>Среднее:</i> {data[1]//data[3] if data[3] > 0 else 0}\n<i>Гарант или 50/50:</i> {"Гарант" if data[2] == 1 else "50/50"}"

    bot.reply_to(message, text, parse_mode = "HTML")

@bot.message_handler(commands = ["pull"])
def pull(message):
    try:
        # Аргументы
        args = getArgs(message.text)
        amount = int(args[1]) if len(args) == 2 and int(args[1]) <= 10 else 10
        name = dbC.getName(args[0])

        # Данные с баз данных databasePortrays и databaseUsers
        count = dbP.getCount(message.from_user.id, name)
        data = list(dbU.getPulls(message.from_user.id)) #current_pulls, all_pulls, guarantee, six_times, six_wins, six_guaranteed
        
        # Переменные
        text = f"<b>Текущий баннер: {makePretty(name)}</b>\n<i>Портретов {makePretty(name)}: {count}</i>"
        chanceIncr = 0

        # Проверка на 6* персонажа
        if name not in dbC.getCharsbyStars("6"): text += "\n<i>Особый режим!</i>"

        # Рулетка редкостей
        for j in range(amount):
            data[0] = data[0] + 1
            data[1] = data[1] + 1

            if data[0] >= 60:
                chanceIncr = 25*(data[0] - 59)
            
            n = randint(1, 1000)
            if 0 <= n <= 15 + chanceIncr or data[0] == 70:
                stars = "6"
                chars = dbC.getCharsbyStars(stars)
            elif 16 + chanceIncr <= n <= 100 + chanceIncr:
                stars = "5"
                chars = dbC.getCharsbyStars(stars)
            elif 101 + chanceIncr <= n <= 500 + 2*chanceIncr:
                stars = "4"
                chars = dbC.getCharsbyStars(stars)
            elif 501 + 2*chanceIncr <= n <= 950:
                stars = "3"
                chars = dbC.getCharsbyStars(stars)
            elif 951 <= n <= 1000:
                stars = "2"
                chars = dbC.getCharsbyStars(stars)

            # Выбор конкретного персонажа и система гаранта/50на50
            if data[2] == 0 and ((0 <= n <= 15 + chanceIncr) or (data[0] == 70)):
                if randint(1, 2) == 1:
                    result = name
                    text += f"\n<b>-- {data[0]} - [{stars}✦] {makePretty(result)} (Победа!)</b>"

                    data[0] = 0
                    data[3], data[4] = data[3] + 1, data[4] + 1

                    dbP.addPortrait(message.from_user.id, name)
                    dbP.updCount(message.from_user.id, name)

                else:
                    try:
                        chars.remove(name)
                    except:
                        pass

                    result = choice(chars) 
                    text += f"\n<b>-- {data[0]} - [{stars}✦] {makePretty(result)} (Проигрыш)</b>"

                    data[0], data[2] = 0, 1
                    data[3] = data[3] + 1

                    dbP.addPortrait(message.from_user.id, result)
                    dbP.updCount(message.from_user.id, result)

                chanceIncr = 0
                data[5] = data[5] + 1

            elif data[2] == 1 and ((0 <= n <= 15 + chanceIncr) or (data[0] == 70)):
                result = name
                text += f"\n<b>-- {data[0]} - [{stars}✦] {makePretty(result)} (Гарант)</b>"

                data[0], data[2] = 0, 0
                data[3], data[5] = data[3] + 1, data[5] + 1
                chanceIncr = 0

                dbP.addPortrait(message.from_user.id, result)
                dbP.updCount(message.from_user.id, name)
            else:
                result = choice(chars)
                text += f"\n({data[0]}) - [{stars}✦] {makePretty(result)}"

        data.append(message.from_user.id)
        dbU.updatePulls(tuple(data))

        bot.reply_to(message, text, parse_mode = 'HTML')
    except dbU.RegistrationError:
        bot.reply_to(message, "Пожалуйста, зарегистрируйтесь в боте через команду /reg или попробуйте снова")
    except LackArgsError:
        bot.reply_to(message, "Пожалуйста, введите имя персонажа, баннер которого вы хотите покрутить и, если хотите, количество круток (до 10) \nНапример: /pull Ан-Ан Ли, 5")
    except dbC.CharNameError:
        bot.reply_to(message, "Проверьте правильность написания имени персонажа или аргументов.\nПример правильного ввода: /pull Ан-Ан Ли, 5")
    except Exception as exc:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
        bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )   

# ----------------- АДМИН-ПАНЕЛЬ И СВЯЗАННЫЕ С НЕЙ ФУНКЦИИ --------------------------------------------------------------------------------------------------------------

# (АДМИН) ПОВЫШЕНИЕ ПОЛЬЗОВАТЕЛЯ ДО АДМИНИСТРАТОРА
@bot.message_handler(commands = ['upgrade'])
def upgrade(message):
    dbU.addUser(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username)
    id = message.reply_to_message.from_user.id
    if isAdmin(message) == True and id not in OWNERS:
        try:
                dbU.upgrade(id)
                bot.reply_to(message, f'Пользователь повышен до администратора.')
         
        except:
                bot.reply_to(message, "Не удалось повысить пользователя до администратора.")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (АДМИН) ПОНИЖЕНИЕ АДМИНА ДО ПОЛЬЗОВАТЕЛЯ
@bot.message_handler(commands = ['downgrade'])
def downgrade(message):
    id = message.reply_to_message.from_user.id
    if isAdmin(message) == True and id not in OWNERS and id != message.from_user.id:
        try:
                dbU.downgrade(id)
                bot.reply_to(message, "Пользователь лишён статуса администратора.")
        except:
                bot.reply_to(message, "Не удалось лишить статуса администратора.")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# ----------------- ФУНКЦИИ ДЛЯ РАБОТЫ С БД  --------------------------------------------------------------------------------------------------------------

# (БД) СПИСОК КОМАНД ПО УПРАВЛЕНИЮ БД И ПРАВАМИ ДОСТУПА
@bot.message_handler(commands = ['adminhelp'])
def adminHelp(message):
    if isAdmin(message) == True:
        text = 'С командами администрации вы можете ознакомиться <a href="https://teletype.in/@m4rkrly/adminhelp">тут</a>\n<i>Лучше смотреть в полноценном браузере</i>.'
        bot.reply_to(message, text, parse_mode = "HTML")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ВЫВОД ВСЕХ ИМЕЮЩИХСЯ В БД ПЕРСОНАЖЕЙ
@bot.message_handler(commands = ['chars'])
def chars(message):
    if isAdmin(message) == True:
        l = ', '.join([i[0] for i in dbC.getNames()])
        bot.reply_to(message, f'<b>Доступные для взаимодействия персонажи</b>\n{l}', parse_mode = "HTML" ) 
    else:
        bot.reply_to(message, "Недостаточно прав!")
# (БД) ВЫВОД ОСНОВНЫХ ДАННЫХ КОНКРЕТНОГО ПЕРСОНАЖА 
@bot.message_handler(commands = ['getchar'])
def getChar(message):
    if isAdmin(message) == True:
        try:
            arg = getArgs(message.text)[0]
            data = dbC.getChar(arg)
            kit = "Нет" if dbK.getKit(arg) == 0 else "Есть"
        except dbC.CharNameError:
            bot.reply_to(message, "Персонаж не найден")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")
        
        if data != None:
            text = f"""
<b>ДАННЫЕ ПЕРСОНАЖА {data[4].split(', ')[0].upper() if data[4] != None else data[0].upper()}</b>\n
<b>Имя:</b> <code>{data[0]}</code>
<b>Редкость:</b> {data[1]}*
<b>Аффлатус:</b> {data[2]}
<b>Тип урона:</b> {data[3]}
<b>Прозвища:</b> {data[4] if data[4] != None else "Не имеется"}
<b>/build:</b> <code>{data[5]}</code>
<b>/materials:</b> <code>{data[6]}</code>
<b>/guide:</b> {data[7]}
<b>/kit:</b> {kit}
<b>R1:</b> <code>{data[8]}</code>
<b>R2:</b> <code>{data[9]}</code>
<b>R3:</b> <code>{data[10]}</code>
                    """
            bot.reply_to(message, text, parse_mode = "HTML")
    else:
        bot.reply_to(message, 'Недостаточно прав!')

# (БД) ДОБАВЛЕНИЕ ПЕРСОНАЖА В БД
@bot.message_handler(commands = ['addchar'])
def addChar(message):
    # name, rarity, afflatus, dmgtype
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text, 4)
            if dbC.getName(args[0]) != 0: raise dbC.RepeationError
            dbC.addChar(args)

            bot.reply_to(message, f"Персонаж {args[0]} был успешно добавлен в базу данных")
        except dbC.RepeationError:
             bot.reply_to(message, "Этот персонаж уже имеется в базе данных!")
        except LackArgsError:
             bot.reply_to(message, "Пожалуйста, введите аргументы: (имя), (редкость), (аффлатус), (тип урона)")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
            bot.send_message(message.chat.id, exc)
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) РЕДАКТИРОВАНИЕ СУЩЕСТВУЮЩЕГО ПЕРСОНАЖА
@bot.message_handler(commands = ["editchar"])
def editChar(message):
    # newName, newRarity, newAfflatus, newDMGType, oldName
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text, 5)
            dbC.editChar(args)

            bot.reply_to(message, f"Данные персонажа {args[0]} были успешно изменены ")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (новое имя), (новая редкость), (новый аффлатус), (новый тип урона), (имя)")
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) УДАЛЕНИЕ ПЕРСОНАЖА
@bot.message_handler(commands = ["delchar"])
def delChar(message):
    # name
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text, 1)[0]
            dbK.delKit(args)
            dbC.delChar(args)

            bot.reply_to(message, f"Данные персонажа {args.lower()} были успешно удалены.")
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ДОБАВЛЕНИЕ ПРОЗВИЩ ПЕРСОНАЖУ
@bot.message_handler(commands = ["addaliases"])
def addAliases(message):
    # name, alias1, alias2 ... aliasN
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text)
            dbC.addAliases(args)
            bot.reply_to(message, f"Прозвища персонажа {args[0]} были успешно изменены.")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя), (прозвище1), (прозвище2)...(прозвищеN)")
        except:
             bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) УДАЛЕНИЕ ВСЕХ(!) ПРОЗВИЩ ПЕРСОНАЖА
@bot.message_handler(commands = ["delaliases"])
def delAliases(message):
    # name
    if isAdmin(message) == True:
        try:
            arg = getArgs(message.text)[0]
            dbC.delAliases(arg)
            bot.reply_to(message, f"Прозвища персонажа {arg} были удалены.")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")

# (БД) ДОБАВЛЕНИЕ КАРТОЧЕК build И materials
@bot.message_handler(content_types = ['photo'])
def addCard(message):
    # [photo] name, type
    if str(message.caption).startswith('/addcard'):
        if isAdmin(message) == True:
            try:
                args = getArgs(message.caption, 2)
                id = message.photo[2].file_id
                dbC.addCard(args[0], args[1], id)
                bot.reply_to(message, f"Выполнено!\nПерсонажу {args[0]} была успешно добавлена карточка!")
            except LackArgsError:
                bot.reply_to(message, "Пожалуйста, введите аргументы: [фотография] - (имя/прозвище), (тип карточки)")
            except dbC.CharNameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addchar или /addaliases")
            except dbC.ArgumentTypeError:
                bot.reply_to(message, "Неправильно выбранный тип изображения: принимаются только build или materials")
            except Exception as exc:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
                bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )   
        else:
            bot.reply_to(message, "Недостаточно прав!")
    
# (БД) ОБНОВЛЕНИЕ РЕЗОНАНСОВ ДЛЯ КАРТОЧЕК
@bot.message_handler(commands = ["addreson"])
def addReson(message):
    if isAdmin(message) == True:
        try:
            # args = message.text[message.text.index(" ") + 1:].split(", ")
            # args[0] = args[0].lower()
            
            args = getArgs(message.text, 3, 0)

            dbC.addReson(args)
            bot.reply_to(message, f"Резонанс №{args[1]} персонажа {args[0]} был изменён")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (номер резонанса), (код резонанса)")
        except dbC.CharNameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except dbC.AmountError:
                bot.reply_to(message, "Неправильно выбранный номер резонанса: принимается только 1, 2 или 3")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )   
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ОБНОВЛЕНИЕ ГАЙДОВ ДЛЯ /guide 
@bot.message_handler(commands = ["addguide"])
def addGuide(message):
    if isAdmin(message) == True:
        try:
            # args = message.text[message.text.index(" ") + 1:].split(", ")
            # args[0] = args[0].lower()
            args = getArgs(message.text, 2)
            dbC.addGuide(args)
            bot.reply_to(message, f"Гайд персонажа {args[0]} был изменён")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (ссылка)")
        except dbC.CharNameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )      
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ОБНОВЛЕНИЕ КИТОВ ПЕРСОНАЖЕЙ
@bot.message_handler(commands = ["addkit"])
def addKit(message):
    if isAdmin(message) == True:
        try:
            args = [0]*4
            data = list(getArgs(message.text))

            args[0], args[1] = data[0], int((data[1].replace(f"{LIBRARYLINK}", "")))
            args[2] = int(data[2]) if len(data) >= 3 else 0
            args[3] = int(data[3]) if len(data) >= 4 else 0

            dbK.addKit(tuple(args))
            bot.reply_to(message, f"Персонажу {args[0]} был успешно добавлен скиллсет.")
            
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (ссылка/ID основного поста скиллсета), (кол-во доп постов с навыками), (кол-во доп постов с эйфорией)")
        except dbC.CharNameError:
            bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addchar или /addaliases")
        except dbC.RepeationError:
            bot.reply_to(message, "/kit этого персонажа уже имеется в базе данных!\nДля замены сначала удалите его с помощью /delkit")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )          
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) УДАЛЕНИЕ КИТОВ ПЕРСОНАЖЕЙ
@bot.message_handler(commands = ["delkit"])
def delkit(message):
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text)[0]
            dbK.delKit(args)
            bot.reply_to(message, f"Скиллсет персонажа {args} был успешно удалён")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")
        except dbC.CharNameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}" )  

    else:
        bot.reply_to(message, "Недостаточно прав!")

@bot.message_handler(commands = ["maddkit"])
def manualAddKit(message):
    # name, post type, id, code of post type
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text, 4)

            if any(i == args[1] for i in KITTYPES[0]) and any(j == args[3] for j in KITTYPES[1]):
                id = dbK.manualAddKit(args)
                bot.reply_to(message, f"Часть /kit персонажа {args[0]} была добавлена в базу данных в строку <code>{id}</code>", parse_mode = "HTML")
            else:
                bot.reply_to(message, "Неверно заданный тип поста/код типа поста.\nИсправьте ввод или ознакомьтесь с /adminhelp перед заполнением")

        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите все необходимые аргументы: (имя), (тип поста), (ID основного поста скиллсета), (код типа поста)")
        except dbC.CharNameError:
            bot.reply_to(message, "Такого имени нет в списке персонажей.\nПроверьте правильность написания с помощью /chars или добавьте персонажа/его прозвище через /addchar или /addaliases")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}")    
    else:
        bot.reply_to(message, "Недостаточно прав!")

@bot.message_handler(commands = ["mdelkit"])
def manualDelKit(message):
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text, 1) 
            dbK.manualDelKit(args) 
            bot.reply_to(message, f"Часть /kit под ID {args[0]} была успешно удалена")
        except LackArgsError:
            bot.reply_to(message, "Пожалуйста, введите все аргументы: (ID строки)")
        except Exception as exc:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода, попробуйте снова или обратитесь к владельцу")  
            bot.send_message(OWNERS[1], f"{exc}, {message.chat.title}, {message.id}")    
    else:
        bot.reply_to(message, "Недостаточно прав!")

# ----------------- ДОПФУНКЦИИ --------------------------------------------------------------------------------------------------------------

@bot.channel_post_handler(content_types = telebot.util.content_type_media)
def forward_post(message):
    try:
        if message.photo != None and message.caption == None: pass
        else:
            bot.forward_message(chat_id = PODVAL[0], message_thread_id = PODVAL[1], from_chat_id = "@stpf_info", message_id = message.id)            
    except Exception as exc:
        bot.send_message(OWNERS[1], f"Что-то не так с пересылкой постов!\n{exc}")

print("Bot has started")
bot.polling(non_stop=True)    