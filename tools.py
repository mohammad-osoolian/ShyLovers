import json
from telegram import Bot, User
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

TOKEN = "5581917717:AAH93gD7cbqlGbXMbuOHEPnBpartWD4aOtA"
USERS = {}

START_TEXT =    ("Hello! \nI made this bot for shy lovers, shy people who may miss their best chances"
                " to have a great relaionship. this is a bot to save those perfect honest relationships"
                "that never start.\nif you love someone and you think she/he truely loves you too and"
                "you are waiting just for a spark to try chance of having eachother, I'm proud to help you!😃"
                "\nWrite /help to explain it for you")


HELP_TEXT = ("You can tell this bot who is your crush and if your crush has crush on you too,"
            " I will tell you both at the same time that you are ready to start a great relationship and this is the spark!✨"
            "\nand if your crush doesn't have crush on you, trust me I will never tell her/him anything :)"
            "\nhere is the list of command that can help you to use this bot:"
            "\n/help : shows this text "
            "\n/setcrush : tell the bot who is your crush "
            # "\n/foundcuples : number of couples found till this moment using this bot :) "
            # "\n/rules : shows the rules of bot and love "
            "\n /cancel : remove your crush from bot and stop every thing"
            "\n /mycrush : show you who you have chosen as your crush in this bot")


SETCRUSH_TEXT = ("Forward a message from him/her to this chat. you can cancel this operation"
                " during it or anythime you want by sending /cancel command.")

CHCKCRUSH_TEXT = "Is this message from your crush?(Y/N)"

CONFIRMCRUSH_YES_TEXT = ("And are you sure that you want to choose this person as"
                        " your crush?(sure/not sure)")

CONFIRMCRUSH_NO_TEXT = "Then forward a message from him/her to this chat."

CONFIRMCHOOSE_YES_TEXT = 'Youre Done!😃\nI hope she/he choose you in the bot too 😄'

CONFIRMCHOOSE_NO_TEXT = "Ok. I canceled it. you have time as much as you need!"

CANCEL_TEXT = ("Ok. I canceled it. no one is specified in this"
                " bot as your crush now. I hope you find the right person soon :)")

MYCRUSH_EMPTY_TEXT = 'no one is selected as your crush.'

def MYCRUSH_TEXT(crush:User):
    return ("this is waht I know about him/her:\n"
    f"\nName: {crush.full_name or 'Unknown'}"
    f"\nUsername: {'@' + crush.username if crush.username else 'Unknown'}"
    f"\ndoes he/she started this bot: {'YES' if crush.id in USERS.keys() else 'NO'}")


def INFORMCUOLE_TEXT(user: User):
    return ("Good news 😁😁😁🌟🌟 you both like eachother😄❤️ go message him/her😁"
            f"\n{user.link or ''}")
