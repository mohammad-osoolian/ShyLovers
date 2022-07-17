from tools import *
from database import *

#status codes:
# 0: new user,
# 1: wating for forward message from crush,
# 2: wating for crush confirm 
# 3: wating for choose confirm
# 4: finished. wating for getting response


def informcuple(userid:int):
    crushid = USERS[userid]['crush']
    user = getuser(userid)
    crush = getuser(crushid)
    user.send_message(INFORMCUOLE_TEXT(crush))
    crush.send_message(INFORMCUOLE_TEXT(user))


def getuser(userid):
    return bot.get_chat_member(chat_id=userid, user_id=userid).user


updater = Updater(TOKEN, use_context=True)
bot = Bot(TOKEN)


def start(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    inituser(userid)
    update.message.reply_text(START_TEXT)

def help(update: Update, context: CallbackContext):
    inituser(update.effective_user.id)
    update.message.reply_text(HELP_TEXT)

def setcrush(update: Update, context: CallbackContext):
    inituser(update.effective_user.id)
    USERS[update.effective_user.id]['st'] = 1
    update.message.reply_text(SETCRUSH_TEXT)


def chckcrush(update: Update, context:CallbackContext):
    if USERS[update.effective_user.id]['st'] != 1:
        return
    USERS[update.effective_user.id]['st'] = 2
    USERS[update.effective_user.id]['crush'] = update.effective_message.forward_from.id
    update.message.reply_text(CHCKCRUSH_TEXT)

def confirmcrush(update: Update, cotext: CallbackContext):
    if USERS[update.effective_user.id]['st'] != 2:
        return
    if update.message.text == 'Y':
        USERS[update.effective_user.id]['st'] = 3
        update.message.reply_text(CONFIRMCRUSH_YES_TEXT)
    elif update.message.text == 'N':
        USERS[update.effective_user.id]['st'] = 1
        update.message.reply_text(CONFIRMCRUSH_NO_TEXT)
    
def confirmchoose(update: Update, cotext: CallbackContext):
    if USERS[update.effective_user.id]['st'] != 3:
        return
    if update.message.text.lower() == 'not sure':
        USERS[update.effective_user.id]['st'] = 0
        USERS[update.effective_user.id]['crush'] = ''
        update.message.reply_text(CONFIRMCHOOSE_NO_TEXT)
    if update.message.text.lower() == 'sure':
        USERS[update.effective_user.id]['st'] = 4
        update.message.reply_text(CONFIRMCHOOSE_YES_TEXT)
    
    result = checkusercrush(update.effective_user.id)
    if result == True:
        informcuple(update.effective_user.id)


def cancel(update: Update, context: CallbackContext):
    inituser(update.effective_user.id)
    update.message.reply_text(CANCEL_TEXT)


def mycrush(update: Update, context: CallbackContext):
    crushid = USERS[update.effective_user.id]['crush']
    if crushid == '':
        update.message.reply_text(MYCRUSH_EMPTY_TEXT)
        return
    crush = getuser(crushid)
    prof = crush.get_profile_photos(0,1)

    if len(prof.photos) > 0:
        update.message.reply_photo(prof.photos[0][0], caption=MYCRUSH_TEXT(crush))
    else:
        update.message.reply_text(MYCRUSH_TEXT(crush))



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('setcrush', setcrush))
updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
updater.dispatcher.add_handler(CommandHandler('mycrush', mycrush))
updater.dispatcher.add_handler(MessageHandler(Filters.text(['Y', 'N']), confirmcrush))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("^(sure|not sure)$"), confirmchoose))
updater.dispatcher.add_handler(MessageHandler(Filters.text &  ~Filters.command, chckcrush))


try:
    conn = connect()
    ctrl = BotUserDBController(conn)
    BotUser.ctrl = ctrl

    updater.start_polling()
    updater.idle()
except Exception as e:
    print(e)

finally:
    conn.commit()
    conn.close()