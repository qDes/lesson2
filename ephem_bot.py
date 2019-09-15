import logging
import ephem

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TOKEN
from settings import PROXY
from datetime import datetime

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def send_planet_constellation(bot, update):
    user_text= update.message.text
    #try to get planet name from text
    try:
        planet_name = user_text.split()[1]
        #create planet instance
        planet = getattr(ephem,planet_name)()
    except (AttributeError, IndexError):
        update.message.reply_text("Try another planet.")
    
    planet.compute(datetime.now())
    constellation = ephem.constellation(planet)[1]
    update.message.reply_text(f'{planet_name} in {constellation} today.')


def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def count_message_words(bot, update):
    user_text = update.message.text
    #count words in message except command
    words_value = len(user_text.split()) - 1
    if words_value > 0:
        update.message.reply_text(words_value)
    else:
        update.message.repy_text("Try another one.")

def get_full_moon(bot, update):
    user_text = update.message.text
    try:
        user_date = datetime.strptime(user_text.split()[1],"%Y-%m-%d")
    except ValueError:
        update.message.reply_text('Date should be in %Y-%m-%d format.')
    full_moon_date = ephem.next_full_moon(user_date)
    update.message.reply_text(full_moon_date)

def main(token, proxy):
    mybot = Updater(token, request_kwargs=proxy)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", send_planet_constellation))
    dp.add_handler(CommandHandler("wordcount", count_message_words))
    dp.add_handler(CommandHandler("next_full_moon", get_full_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main(TOKEN,PROXY)
