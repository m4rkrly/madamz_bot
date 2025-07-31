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

bot = TeleBot(TOKEN)

# ----------------- САБФУНКЦИИ ------------------------------------------------------------------------------------------

# (АДМИН) ПРОВЕРКА ЯВЛЯЕТСЯ ЛИ ПОЛЬЗОВАТЕЛЬ АДМИНИСТРАТОРОМ/ВЛАДЕЛЬЦЕМ
def isAdmin(message):
    if dbU.isAdmin(message.from_user.id) == (1,) or message.from_user.id in OWNERS:
        return True
    else: 
        return False

# (БД) ПОЛУЧЕНИЕ АРГУМЕНТОВ ДЛЯ ЗАНЕСЕНИЯ В БД
def getArgs(raw):
    try:
        raw = raw[raw.index(" ") + 1:]
        return tuple([a.lower() for a in raw.split(', ')])
    except:
        return "0"

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
    text = "<b>Приветствую!</b>\nВы можете ознакомиться с доступными командами через команду /help и зарегистрироваться через команду /reg."

    bot.send_message(message.chat.id, text, parse_mode = "HTML")

# РЕГИСТРАЦИЯ
@bot.message_handler(commands = ["reg"])
def reg(message):
    try: 
        dbU.addUser(message.from_user.id, message.from_user.username)
        
        bot.reply_to(message, "Вы были успешно зарегистрированы!")
        # print(f'{message.from_user.id} ({message.from_user.username}) has registered')
    except:
        bot.reply_to(message, "Не удалось зарегистрировать")
        # print(f'Something went wrong in registration of {message.from_user.id} ({message.from_user.username})')

# ОБЩАЯ ПОМОЩЬ
@bot.message_handler(commands = ["help"])
def help(message):
    text = [
    """
<b>ПОЛЬЗОВАТЕЛЬСКИЕ КОМАНДЫ</b>
<i>Все аргументы в командах пишутся через запятую с пробелом!</i>
/reg - зарегистрироваться в боте (для /pull)
<code>/pull</code> [имя 6* персонажа] - покрутить баннер с персонажем (перед этим нужно использовать /reg) <b>(ТОЛЬКО В ТОПИКЕ ГАЧАРОЛЛ)</b>
/mypulls - узнать свою статистику по круткам 
<code>/smooch</code> [имя персонажа] - поцеловать персонажа
<code>/link</code> [<code>ru</code>, <code>cn</code>, <code>con</code>] - получить ссылку на канал: Фонд, Китайка, Конундрум
<code>/prydwen</code> [имя персонажа] - получить ссылку на персонажа на Prydwen
/buildhelp - получить список персонажей, имеющих карточки в /build
<code>/build</code> [имя персонажа] - получить карточки билда персонажа
/kithelp - получить список персонажей, имеющих /kit
<code>/kit</code> [имя персонажа], [<code>i</code> - инсайт, <code>s</code> - навыки, <code>p</code> - портреты, <code>u</code> - ультимейт, <code>e</code> - эйфория] - получить перевод скиллсета персонажа или отдельные его части
<code>/guide</code> [имя персонажа] - получить гайд на персонажа
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
        bot.reply_to(message, "Такого персонажа нет.")

# ВЫВОД ГАЙДА ДЛЯ ПЕРСОНАЖА (/guide)
@bot.message_handler(commands = ["guide"])
def guide(message):
    try:
        arg = message.text[message.text.index(' ') + 1:]
        data = dbC.getGuide(arg)
        bot.reply_to(message, f'{data[0]}')
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище персонажа)")
    except NameError:
        bot.reply_to(message, "К сожалению, гайда на этого персонажа пока нет")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
        # print(f"Something went wrong in getting guide of {arg}") 

# ВЫВОД КАРТОЧКИ ПРОКАЧКИ И МАТЕРИАЛОВ ДЛЯ ПЕРСОНАЖА (/build)
@bot.message_handler(commands = ['build'])
def build(message):
    try:
        arg = getArgs(message.text)[0]
        data = dbC.getPics(arg)
        text = str()
        if data[-2] != '0':
            text = f"<b>Коды резонансов</b>\nR1: <code>{data[-2]}</code>"
        if data[-1] != "0":
            text += f"R2: <code>{data[-1]}</code>"
        if data[1] == '0':
            # bot.send_photo(message.chat.id, photo=data[0], caption = text, parse_mode = "HTML")
            pics = [InputMediaPhoto(data[0], caption = text, parse_mode="HTML")]
        else:
            pics = [InputMediaPhoto(data[0], caption = text, parse_mode="HTML"), InputMediaPhoto(data[1])]
        bot.send_media_group(message.chat.id, pics, message_thread_id = message.message_thread_id)

    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище персонажа)")
    except NameError:
        bot.reply_to(message, "К сожалению, карточки этого персонажа пока нет")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
        # print(f"Something went wrong in getting cards and resonances of {arg}")

# ВЫВОД ВСЕХ ДОСТУПНЫХ ПЕРСОНАЖЕЙ ДЛЯ /build
@bot.message_handler(commands = ['buildhelp'])
def buildhelp(message):
    try:
        data = dbC.getBuildableAliases()
        data = [f'<code>{a}</code>' for a in data]
        text = ", ".join(data)

        bot.reply_to(message, f"<b>Персонажи, доступные для команды <code>/build</code></b>\n{text}", parse_mode = "HTML")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

# ВЫВОД СКИЛЛСЕТОВ ПЕРСОНАЖЕЙ (/kit)
@bot.message_handler(commands = ['kit'])
def kit(message):
    try:
        args = getArgs(message.text)
        data = dbK.getKit(args[0])

        if len(args) == 1:
            id = data[0]
            bot.forward_message(chat_id = message.chat.id, message_thread_id= message.message_thread_id, from_chat_id = f"{LIBRARY}", message_id = int(id[0]))
                
        elif len(args) == 2 and args[1] in ('i', 's', 'p', 'u', 'e'):
            for id in data:
                if id[1] == args[1]: bot.forward_message(chat_id = message.chat.id, message_thread_id= message.message_thread_id, from_chat_id = f"{LIBRARY}", message_id = int(id[0]))
        else:
            bot.reply_to(message, "Неправильный ввод")
    except NameError:
        bot.reply_to(message, "К сожалению, скиллсета этого персонажа нет")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

@bot.message_handler(commands = ['kithelp'])
def kitHelp(message):
    try:
        data = set([i[0] for i in dbK.getAllKits()])
        data = [f'<code>{dbC.getTranslatedAlias(j)}</code>' for j in data]
        data = ', '.join(data)
        
        bot.reply_to(message, f"<b>Список персонажей, доступных для <code>/kit</code>:</b>\n{data}", parse_mode = "HTML")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")

# ----------------- КРУТКИ И РАЗВЛЕКАТЕЛЬНЫЕ ФУНКЦИИ --------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands = ['smooch'])
def smooch(message):
    try:
        args = getArgs(message.text)[0]
        smooches = dbC.smooch(args)
        alias = makePretty(args)

        bot.reply_to(message, f"Вы поцеловали {alias}! Теперь на нём/ней {smooches} поцелуев")
    except NameError:
        bot.reply_to(message, "К сожалению, этого персонажа нет")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")


# @bot.message_handler(commands = ['pull'])
# def pull(message):
#     args = getArgs(message.text)[0]

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

                # print(f'{id} ({message.reply_to_message.from_user.username}) was upgraded to Admin by {message.from_user.id} ({message.from_user.username})')
            
        except:
                bot.reply_to(message, "Не удалось повысить пользователя до администратора.")

                # print(f"Something went wrong in upgrading {id} ({message.reply_to_message.from_user.username}) to Admin")
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

                # print(f'{id} ({message.reply_to_message.from_user.username}) was downgraded to User by {message.from_user.id} ({message.from_user.username})')

        except:
                bot.reply_to(message, "Не удалось лишить статуса администратора.")

            # print(f"Something went wrong in downgrading {id} ({message.reply_to_message.from_user.username}) to User")
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
        except:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")
        data = dbC.getChar(arg)
        kit = "Нет" if dbK.getKit(arg) == [] else "Есть"
    
        if data != None:
            text = f"""
<b>ДАННЫЕ ПЕРСОНАЖА {data[4].split(', ')[0].upper()}</b>\n
<b>Имя:</b> <code>{data[0]}</code>
<b>Редкость:</b> {data[1]}*
<b>Аффлатус:</b> {data[2]}
<b>Тип урона:</b> {data[3]}
<b>Прозвища:</b> {data[4]}
<b>/build:</b> <code>{data[5]}</code>
<b>/materials:</b> <code>{data[6]}</code>
<b>/guide:</b> {data[7]}
<b>/kit:</b> {kit}
<b>R1:</b> <code>{data[8]}</code>
<b>R2:</b> <code>{data[9]}</code>
                    """
            bot.reply_to(message, text, parse_mode = "HTML")
        else:
            bot.reply_to(message, "Данные не найдены")
    else:
        bot.reply_to(message, 'Недостаточно прав!')

# (БД) ДОБАВЛЕНИЕ ПЕРСОНАЖА В БД
@bot.message_handler(commands = ['addchar'])
def addChar(message):
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text)
            if dbC.getName(args[0]) != 0:
                 raise NameError
            dbC.addChar(args)

            bot.reply_to(message, f"Персонаж {args[0]} был успешно добавлен в базу данных")
            # print(f'{message.from_user.id} ({message.from_user.username}) has added character in database: {args})')
        except NameError:
             bot.reply_to(message, "Этот персонаж уже имеется в базе данных!")
        except ValueError:
             bot.reply_to(message, "Пожалуйста, введите аргументы: (имя), (редкость), (аффлатус), (тип урона)")
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
            # print(f'Something went wrong in adding a character by {message.from_user.id} ({message.from_user.username})')
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) РЕДАКТИРОВАНИЕ СУЩЕСТВУЮЩЕГО ПЕРСОНАЖА
@bot.message_handler(commands = ["editchar"])
def editChar(message):
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text)
            dbC.editChar(args)

            bot.reply_to(message, f"Данные персонажа {args[0]} были успешно изменены ")
            # print(f'{message.from_user.id} ({message.from_user.username}) has changed character {args[-1]} in database on: {args})')
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (новое имя), (новая редкость), (новый аффлатус), (новый тип урона), (имя)")
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
            # print(f'Something went wrong in editing a character by {message.from_user.id} ({message.from_user.username})') 
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) УДАЛЕНИЕ ПЕРСОНАЖА
@bot.message_handler(commands = ["delchar"])
def delChar(message):
    if isAdmin(message) == True:
        try:
            args = message.text[9:]
            dbC.delChar(args.lower())

            bot.reply_to(message, f"Данные персонажа {args.lower()} были успешно удалены.")
            # print(f'{message.from_user.id} ({message.from_user.username}) has deleted character {args.lower()}')
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
            # print(f'Something went wrong in deleting a character by {message.from_user.id} ({message.from_user.username})')

# (БД) ДОБАВЛЕНИЕ ПРОЗВИЩ ПЕРСОНАЖУ
@bot.message_handler(commands = ["addaliases"])
def addAliases(message):
    if isAdmin(message) == True:
        try:
            args = getArgs(message.text)
            dbC.addAliases(args)
            bot.reply_to(message, f"Прозвища персонажа {args[0]} были успешно изменены.")
            # print(f'{message.from_user.id} ({message.from_user.username}) has changed aliases of character {args[0]}')
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя), (прозвище1), (прозвище2)...(прозвищеN)")
        except:
            bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")
            # print(f'Something went wrong in adding aliases to a character by {message.from_user.id} ({message.from_user.username})')
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) УДАЛЕНИЕ ВСЕХ(!) ПРОЗВИЩ ПЕРСОНАЖА
@bot.message_handler(commands = ["delaliases"])
def delAliases(message):
    if isAdmin(message) == True:
        try:
            arg = getArgs(message.text)[0]
            dbC.delAliases(arg)
            bot.reply_to(message, f"Прозвища персонажа {arg} были удалены.")
            # print(f"{message.from_user.id} ({message.from_user.username}) has deleted all aliases of {arg}")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")

# (БД) ДОБАВЛЕНИЕ КАРТОЧЕК build И materials
@bot.message_handler(content_types = ['photo'])
def addCard(message):
    if str(message.caption).startswith('/addcard'):
        if isAdmin(message) == True:
            try:
                args = getArgs(message.caption)
                id = message.photo[2].file_id
                dbC.addCard(args[0], args[1], id)
                bot.reply_to(message, f"Выполнено!\nПерсонажу {args[0]} была успешно добавлена карточка!")
            except ValueError:
                bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (тип карточки)")
            except NameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addchar или /addaliases")
            except Exception:
                bot.reply_to(message, "Неправильно выбранный тип изображения: принимаются только build или materials")
            except:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")    
        else:
            bot.reply_to(message, "Недостаточно прав!")
    
# (БД) ОБНОВЛЕНИЕ РЕЗОНАНСОВ ДЛЯ КАРТОЧЕК
@bot.message_handler(commands = ["addreson"])
def addReson(message):
    if isAdmin(message) == True:
        try:
            args = message.text[message.text.index(" ") + 1:].split(", ")
            args[0] = args[0].lower()
            
            dbC.addReson(args)
            bot.reply_to(message, f"Резонанс №{args[1]} персонажа {args[0]} был изменён")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (номер резонанса), (код резонанса)")
        except NameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except Exception:
                bot.reply_to(message, "Неправильно выбранный номер резонанса: принимается только 1 или 2")
        except:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")    
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ОБНОВЛЕНИЕ ГАЙДОВ ДЛЯ /guide 
@bot.message_handler(commands = ["addguide"])
def addGuide(message):
    if isAdmin(message) == True:
        try:
            args = message.text[message.text.index(" ") + 1:].split(", ")
            args[0] = args[0].lower()
            dbC.addGuide(args)
            bot.reply_to(message, f"Гайд персонажа {args[0]} был изменён")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (ссылка)")
        except NameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")       
    else:
        bot.reply_to(message, "Недостаточно прав!")

# (БД) ОБНОВЛЕНИЕ КИТОВ ПЕРСОНАЖЕЙ
@bot.message_handler(commands = ["addkit"])
def addKit(message):
    if isAdmin(message) == True:
        try:
            args = list(getArgs(message.text))
            args[1] = int((args[1].replace(f"{LIBRARYLINK}", "")))
            args[2], args[3] = int(args[2]), int(args[3])
            dbK.addKit(tuple(args))
            bot.reply_to(message, f"Персонажу {args[0]} был успешно добавлен скиллсет.")
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище), (ссылка/ID основного поста скиллсета), (кол-во доп постов с навыками), (кол-во доп постов с эйфорией)")
        except NameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")           
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
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите аргументы: (имя/прозвище)")
        except NameError:
                bot.reply_to(message, "Такого имени нет в базе данных.\nПроверьте правильность написания или добавьте персонажа/его прозвище через /addChar или /addAliases")
        except:
                bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")  
    else:
        bot.reply_to(message, "Недостаточно прав!")

# ----------------- ДОПФУНКЦИИ --------------------------------------------------------------------------------------------------------------

@bot.channel_post_handler(func = lambda message: True)
def forward_post(message):
    try:
        bot.forward_message(chat_id = PODVAL[0], message_thread_id = PODVAL[1], from_chat_id = "@stpf_info", message_id = message.id)
    except:
        bot.send_message(OWNERS[1], "Что-то не так с пересылкой постов!")

@bot.message_handler(commands = ["mypulls"])
def mypulls(message):
    data = dbU.getPulls(message.from_user.id)
    
    text = f"<b>Приветствую, {message.from_user.username if message.from_user.username != None else "Пользователь"}!</b>\n<i>Всего:</i> {data[1]}, <i>Откручено:</i> {data[0]}\nW/G/A = {data[4]}/{data[5]}/{data[3]}, <i>Среднее:</i> {data[1]//data[3] if data[3] > 0 else 0}\n<i>Гарант или 50/50:</i> {"Гарант" if data[2] == 1 else "50/50"}"

    bot.reply_to(message, text, parse_mode = "HTML")

@bot.message_handler(commands = ["pull"])
def pull(message):
    try:
        arg = getArgs(message.text)[0]
        name = dbC.getName(arg)
        dbP.addPortrait(message.from_user.id, name)
        count = dbP.getCount(message.from_user.id, name)[0]
        text = f"<b>Текущий баннер: {makePretty(name)}</b>\n<i>Портретов {makePretty(name)}: {count}</i>"
        chanceIncr = 0

        for j in range(10):
            data = list(dbU.getPulls(message.from_user.id)) #current_pulls, all_pulls, guarantee, six_times, six_wins, six_guaranteed

            data[0] = data[0] + 1
            data[1] = data[1] + 1

            if data[0] >= 60:
                chanceIncr = 25*(data[0] - 59)
            
            n = randint(1, 1000)
            if 0 <= n <= 15 + chanceIncr or data[0] == 70:
                stars = "6"
                chars = dbC.getCharsbyStars(stars)
            elif 16 + chanceIncr <= n <= 100:
                stars = "5"
                chars = dbC.getCharsbyStars(stars)
            elif 101 + chanceIncr <= n <= 500:
                stars = "4"
                chars = dbC.getCharsbyStars(stars)
            elif 501 + chanceIncr <= n <= 950:
                stars = "3"
                chars = dbC.getCharsbyStars(stars)
            elif 951 <= n <= 1000:
                stars = "2"
                chars = dbC.getCharsbyStars(stars)

            if data[2] == 0 and ((0 <= n <= 15 + chanceIncr) or (data[0] == 70)):
                if randint(1, 2) == 1:
                    result = name
                    text += f"\n<b>-- {data[0]} - [{stars}✦] {makePretty(result)} (Победа!)</b>"
                    data[0] = 0
                    data[3], data[4] = data[3] + 1, data[4] + 1
                    dbP.updCount(message.from_user.id, name)

                else:
                    chars.remove(name)
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
                dbP.updCount(message.from_user.id, name)
            else:
                result = choice(chars)
                text += f"\n({data[0]}) - [{stars}✦] {makePretty(result)}"

            data.append(message.from_user.id)
            dbU.updatePulls(tuple(data))

        bot.reply_to(message, text, parse_mode = 'HTML')
    except TypeError:
        bot.reply_to(message, "Пожалуйста, введите имя 6✦-го персонажа, баннер которого вы хотите покрутить\nНапример: /pull Ан-Ан Ли")
    except:
        bot.reply_to(message, "Нетипичная ошибка: проверьте правильность ввода или обратитесь к владельцу")  

print("Bot has started")
bot.polling(non_stop=True)       