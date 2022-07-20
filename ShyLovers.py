from dotenv import load_dotenv
load_dotenv()

from tools import *
from database import *


#status codes:
# 0: new user,
# 1: wating for forward message from crush,
# 2: wating for crush confirm 
# 3: wating for choose confirm
# 4: finished. wating for getting response


def informcuple(userid:int):
    crushid = BotUser(userid).csh
    user = getfulluser(userid)
    crush = getfulluser(crushid)
    user.send_message(INFORMCUOLE_TEXT(crush,BotUser(userid).lng))
    crush.send_message(INFORMCUOLE_TEXT(user,BotUser(crushid).lng))


def getfulluser(userid):
    return bot.get_chat_member(chat_id=userid, user_id=userid).user


def start(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    if not BotUser.isuser(userid):
        BotUser.newuser(userid)
    usr = BotUser(userid)
    update.message.reply_text(START_TEXT(usr.lng), reply_markup=SETLANG_KEYBOARD())

def filter_button(update:Update, context: CallbackContext):
    data = update.callback_query.data
    if data in ['en', 'far']:
        lang_button(update, context)
    elif data in ['chckcrush_yes', 'chckcrush_no']:
        confirmcrush_button(update, context)
    elif data in ['confirmcrush_yes', 'confirmcrush_no']:
        confirmchoose_button(update, context)

def lang_button(update:Update, context: CallbackContext):
    usr = BotUser(update.effective_user.id)
    query = update.callback_query
    query.answer()
    lang = query.data
    usr.lng = lang
    if query.message.text == START_TEXT('en') or query.message.text == START_TEXT('far'):
        query.edit_message_text(text=START_TEXT(usr.lng))
    elif query.message.text == SETLANG_TEXT('en') or query.message.text == SETLANG_TEXT('far'):
        query.edit_message_text(text=SETLANG_AFTER_TEXT(usr.lng))

def confirmcrush_button(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    usr = BotUser(update.effective_user.id)
    if usr.st != 2:
        return
    if data == 'chckcrush_yes':
        usr.st = 3
        query.edit_message_text(CONFIRMCRUSH_YES_TEXT(usr.lng), reply_markup=CONFIRMCRUSH_YES_KEYBOARD(usr.lng))
    elif data == 'chckcrush_no':
        usr.st = 1
        usr.csh = None
        query.edit_message_text(CONFIRMCRUSH_NO_TEXT(usr.lng))

def confirmchoose_button(update: Update, cotext: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    usr = BotUser(update.effective_user.id)
    if usr.st != 3:
        return
    if data == 'confirmcrush_yes':
        usr.st = 4
        query.edit_message_text(CONFIRMCHOOSE_YES_TEXT(usr.lng))
    if data == 'confirmcrush_no':
        usr.clear()
        query.edit_message_text(CONFIRMCHOOSE_NO_TEXT(usr.lng))
    
    result = usr.ismatched()
    if result == True:
        informcuple(update.effective_user.id)

def help(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    if not BotUser.isuser(userid):
        BotUser.newuser(userid)
    usr = BotUser(userid)
    update.message.reply_text(HELP_TEXT(usr.lng))

def setcrush(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    if not BotUser.isuser(userid):
        BotUser.newuser(userid)
    usr = BotUser(userid)
    usr.st = 1
    update.message.reply_text(SETCRUSH_TEXT(usr.lng))


def chckcrush(update: Update, context:CallbackContext):
    usr = BotUser(update.effective_user.id)
    if usr.st != 1:
        return
    if update.effective_message.forward_from == None:
        update.message.reply_text(SETCRUSH_HIDE_TEXT(usr.lng))
        return
    crushid = update.effective_message.forward_from.id
    if usr.id == crushid:
        return
    usr.csh = crushid
    usr.st = 2
    update.message.reply_text(CHCKCRUSH_TEXT(usr.lng), 
                              reply_markup=CHCKCRUSH_KEYBOARD(usr.lng),
                              reply_to_message_id=update.message.message_id)
 

def cancel(update: Update, context: CallbackContext):
    userid = update.effective_user.id
    if not BotUser.isuser(userid):
        BotUser.newuser(userid)
    usr = BotUser(userid)
    usr.clear()
    update.message.reply_text(CANCEL_TEXT(usr.lng))


def mycrush(update: Update, context: CallbackContext):
    usr = BotUser(update.effective_user.id)
    crushid = usr.csh
    if crushid == None:
        update.message.reply_text(MYCRUSH_EMPTY_TEXT(usr.lng))
        return
    crush = getfulluser(crushid)
    prof = crush.get_profile_photos(0,1)

    if len(prof.photos) > 0:
        update.message.reply_photo(prof.photos[0][0], caption=MYCRUSH_TEXT(crush,BotUser.isuser(crush.id), BotUser(usr.id).lng))
    else:
        update.message.reply_text(MYCRUSH_TEXT(crush,BotUser.isuser(crush.id), BotUser(usr.id).lng))

def setlang(update: Update, context: CallbackContext):
    usr = BotUser(update.effective_user.id)
    update.message.reply_text(SETLANG_TEXT(usr.lng), reply_markup=SETLANG_KEYBOARD())

updater = Updater(TOKEN, use_context=True)
bot = Bot(TOKEN)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(filter_button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('setcrush', setcrush))
updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
updater.dispatcher.add_handler(CommandHandler('mycrush', mycrush))
updater.dispatcher.add_handler(CommandHandler('setlang', setlang))
# updater.dispatcher.add_handler(MessageHandler(Filters.text(['Y', 'N']), confirmcrush))
# updater.dispatcher.add_handler(MessageHandler(Filters.regex("^(sure|not sure)$"), confirmchoose))
updater.dispatcher.add_handler(MessageHandler(Filters.text &  ~Filters.command, chckcrush))


try:
    conn = connect()
    ctrl = BotUserDBController(conn)
    BotUser.ctrl = ctrl

    updater.start_webhook(  listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN,
                            webhook_url="https://shylovers.herokuapp.com/" + TOKEN)
    print('Bot is ON')
    updater.idle()
except Exception as e:
    print(e)

finally:
    conn.commit()
    conn.close()