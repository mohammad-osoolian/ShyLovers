from telegram import Bot, User, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.filters import Filters
import os

TOKEN = os.getenv('TOKEN')

PORT = int(os.environ.get('PORT', 8443))

START_TEXT_DICT = {'en':("Hello! \nI made this bot for shy lovers, shy people who may miss their best chances"
                        " to have a great relaionship. this is a bot to save those perfect relationships"
                        " that never start.\nif you love someone and you think she/he truely loves you too and"
                        " you are waiting just for a spark to try chance of having eachother, I'm proud to help you!😃"
                        "\nWrite /help to explain it for you"),
                    'far':('سلام! \n من این ربات رو برای عاشق های خجالتی ساختم. آدمایی که ممکنه به خاطر'
                        ' خجالتی بودن شانسشون رو برای داشتن یک عشق عالی از دست بدن.'
                        ' این ربات برای نجات دادن رابطه های صمیمانه ایه که هیچ وقت شروع نشدن.'
                        '\nاگر عاشق کسی شدی و فکر میکنی که اونم هم عاشقت شده و تنها منتظر یک جرقه هستین'
                        ' که از شانس با هم بودن بهره مند بشین، باعث افتخاره که بهت کمک کنم😃'
                        '\nدستور /help رو وارد کن تا بیشتر بهت توضیح بدم.')
}

SETLANG_TEXT_DICT = {'en':"Please choose the language for bot:",
                     'far': "لطفا زبان بات را انتخاب کنید:"
}

SETLANG_AFTER_TEXT_DICT = {'en':"Language is English now.",
                            'far':"زبان بات فارسی است."
}

HELP_TEXT_DICT = {'en':("You can tell this bot who is your crush and if your crush has crush on you too,"
                        " I will tell you both at the same time that you are ready to start a great relationship and this is the spark!✨"
                        "\nand if your crush doesn't have crush on you, trust me I will never tell her/him anything :)"
                        "\n\n\nhere is the list of command that can help you to use this bot:"
                        "\n/help : shows this text "
                        "\n/setlang : set language of bot "
                        "\n/setcrush : tell the bot who is your crush "
                        "\n /cancel : remove your crush from bot and stop every thing"
                        "\n /mycrush : show you who you have chosen as your crush in this bot"),
                  'far': ('تو میتونی به این بات بگی که روی چه کسی کراش داری و اگر اون شخص هم روی توی کراش داشت،'
                        ' من هم زمان به هر دوتاتون خبر میدم که شما به هم علاقه دارین و'
                        ' و آماده اید که یک رابطه قشنگ رو شروع کنید و این همون جرقه ای هست که بهش احتیاج داشتید✨'
                        '\nاما اگر اونی که تو بهش علاقه مندی به تو علاقه مند نبود، خیالت تخت من هیچی بهش نمیگم :)'
                        '\n\n\nاین لیست دستورات بات هست که میتونه کمکت کنه از بات استفاده کنی:'
                        '\n/help : این متن رو نمایش میده'
                        '\n/setlang : زبان ربات رو تنظیم میکنه'
                        '\n/setcrush : میتونی به رباتت بگی به کی علاقه داری'
                        '\n/cancel : کراشت رو از حافظه ربات پاک میکنه و همه چی رو متوقف میکنه'
                        '\n/mycrush : ربات هر چیزی در مورد کراشت میدونه بهت میگه')
}

SETCRUSH_TEXT_DICT = {'en':("Forward a message from him/her to this chat. you can cancel this operation"
                            " during it or anythime you want by sending /cancel command."),
                      'far':('یک پیام ازش به این ربات فروارد کن تا بشناسمش. میتونی این عملیات رو'
                             ' حین انجامش یا هر وقت که خواستی با دستور /cancel متوقف کنی.')
}

SETCRUSH_HIDE_TEXT_DICT = {'en':('Unfortunately this user has hide profile and there is no way to be recognized.'
                                 '\nWe are going to make it possible to recognize hide profiles with username.'
                                 '\nWait for next update...!'),
                            'far':('متاسفانه اکانت این کاربر هاید هست و نمیتونیم متوجه بشیم کیه.'
                                    ' اما داریم سعی میکنیم که کاربر ها رو نام کاربریشون بشناسیم تا این مشکل رو حل کنیم.'
                                    '\nمنتظر آپدیت بعدی باش...!')}

CHCKCRUSH_TEXT_DICT = {'en':"Is this message from your crush?",
                        'far':'این پیام از طرف کراشت هست؟'
}

CONFIRMCRUSH_YES_TEXT_DICT = {'en':("And are you sure that you want to choose this person as"
                                    " your crush?"),
                             'far':'و آیا مطمئنی که این آدم رو با قلبت دوستش داری؟'  
}

CONFIRMCRUSH_NO_TEXT_DICT = {'en':"Then forward a message from him/her to this chat.",
                            'far':'پس لطفا یک پیام ازش به این چت فروارد کن.'
}

CONFIRMCHOOSE_YES_TEXT_DICT = {'en': 'Youre Done!😃\nI hope she/he choose you in the bot too 😄',
                              'far':'تموم شد 😃\nامیدوارم که اون هم تورو دوست داشته باشه و توی بات انتخابت کنه 😄'
}

CONFIRMCHOOSE_NO_TEXT_DICT = {'en':"Ok. I canceled it. you have time as much as you need!",
                                'far':'خیله خب. پس من فعلا کنسلش کردم تا با آرامش فکراتو بکنی. هر وقت انتخابتو کردی، اگه بهم نیاز داشتی در دسترستم :)'
}

CANCEL_TEXT_DICT = {'en':("Ok. I canceled it. no one is specified in this"
                          " bot as your crush now. I hope you find the right person soon :)"),
                    'far':'خیله خب. کنسل شد. حالا بات هیچ کسو به عنوان کراش تو نمیشناسه. امیدوارم هر چه زود تر شخص مناسبت رو پیدا کنی :)'
}

MYCRUSH_EMPTY_TEXT_DICT = {'en': 'no one is selected as your crush.',
                            'far':'هیچ کسی به عنوان کراشت توی بات وجود نداره.'
}

def MYCRUSH_TEXT_EN(crush:User, isuser:bool):
    return ("this is waht I know about him/her:\n"
            f"\nName: {crush.full_name or 'Unknown'}"
            f"\nUsername: {'@' + crush.username if crush.username else 'Unknown'}"
            f"\ndoes he/she started this bot: {'YES' if isuser else 'NO'}")

def MYCRUSH_TEXT_FAR(crush:User, isuser:bool):
    return ('این تمام چیزیه که ازش میدونم:\n'
            f"\nاسم: {crush.full_name or 'ناشناس'}"
            f"\nنام کاربری: {'@' + crush.username if crush.username else 'ناشناس'}"
            f"\nآیا بات را استارت زده: {'بله' if isuser else 'خیر'}")

MYCRUSH_TEXT_DICT = {'en':MYCRUSH_TEXT_EN, 'far':MYCRUSH_TEXT_FAR}

def INFORMCUOLE_TEXT_EN(user: User):
    return ("Good news 😁😁😁🌟🌟 you both like eachother😄❤️ go message him/her😁"
            f"\n{user.link or ''}")

def INFORMCUOLE_TEXT_FAR(user: User):
    return ("خبرای خوب دارم 😁😁😁🌟🌟 هر دوتاتون به هم دیگه علاقه دارین 😄❤️ برو بهش پیام بده! 😁"
            f"\n{user.link or ''}")

INFORMCUOLE_TEXT_DICT = {'en':INFORMCUOLE_TEXT_EN, 'far':INFORMCUOLE_TEXT_FAR}

CHCKCRUSH_KEYBOARD_DICT = {'en':[
                                    [
                                        InlineKeyboardButton("Yes", callback_data="chckcrush_yes"),
                                    ],
                                    [
                                        InlineKeyboardButton("No", callback_data="chckcrush_no"),
                                    ]
                                ],
                         'far': [
                                    [
                                        InlineKeyboardButton("آره", callback_data="chckcrush_yes"),
                                    ],
                                    [
                                        InlineKeyboardButton("نه", callback_data="chckcrush_no"),
                                    ]
                                ]}

CONFIRMCRUSH_YES_KEYBOARD_DICT = {'en': [
                                            [
                                                InlineKeyboardButton("Yes I'm sure", callback_data="confirmcrush_yes"),
                                            ],
                                            [
                                                InlineKeyboardButton("I'm not sure", callback_data="confirmcrush_no"),
                                            ]
                                        ],
                                  'far':[
                                            [
                                                InlineKeyboardButton("مطمئنم", callback_data="confirmcrush_yes"),
                                            ],
                                            [
                                                InlineKeyboardButton("نه", callback_data="confirmcrush_no"),
                                            ]
                                        ]}

SETLANG_KEYBOARD_HARD = [
                            [
                                InlineKeyboardButton("فارسی", callback_data="far"),
                                InlineKeyboardButton("English", callback_data="en"),
                            ],
                        ]

def START_TEXT(lang):
    return START_TEXT_DICT[lang]

def SETLANG_TEXT(lang):
    return SETLANG_TEXT_DICT[lang]

def SETLANG_AFTER_TEXT(lang):
    return SETLANG_AFTER_TEXT_DICT[lang]

def HELP_TEXT(lang):
    return HELP_TEXT_DICT[lang]

def SETCRUSH_TEXT(lang):
    return SETCRUSH_TEXT_DICT[lang]

def SETCRUSH_HIDE_TEXT(lang):
    return SETCRUSH_HIDE_TEXT_DICT[lang]

def CHCKCRUSH_TEXT(lang):
    return CHCKCRUSH_TEXT_DICT[lang]

def CONFIRMCRUSH_YES_TEXT(lang):
    return CONFIRMCRUSH_YES_TEXT_DICT[lang]                 

def CONFIRMCRUSH_NO_TEXT(lang):
    return CONFIRMCRUSH_NO_TEXT_DICT[lang]

def CONFIRMCHOOSE_YES_TEXT(lang):
    return CONFIRMCHOOSE_YES_TEXT_DICT[lang]    

def CONFIRMCHOOSE_NO_TEXT(lang):
    return CONFIRMCHOOSE_NO_TEXT_DICT[lang]

def CANCEL_TEXT(lang):
    return CANCEL_TEXT_DICT[lang]

def MYCRUSH_EMPTY_TEXT(lang):
    return MYCRUSH_EMPTY_TEXT_DICT[lang]

def MYCRUSH_TEXT(crush:User, isuser:bool, lang):
    return MYCRUSH_TEXT_DICT[lang](crush, isuser)

def INFORMCUOLE_TEXT(user: User, lang):
    return INFORMCUOLE_TEXT_DICT[lang](user)

# --------------------------------------------------------------------

def SETLANG_KEYBOARD():
    keyboard = SETLANG_KEYBOARD_HARD
    return InlineKeyboardMarkup(keyboard)

def CHCKCRUSH_KEYBOARD(lang):
    keyboard = CHCKCRUSH_KEYBOARD_DICT[lang]
    return InlineKeyboardMarkup(keyboard)

def CONFIRMCRUSH_YES_KEYBOARD(lang):
    keyboard = CONFIRMCRUSH_YES_KEYBOARD_DICT[lang]
    return InlineKeyboardMarkup(keyboard)
