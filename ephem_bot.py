import logging
import functools
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TOKEN
from settings import PROXY

from bot_functions import greet_user
from bot_functions import send_planet_constellation
from bot_functions import talk_to_me
from bot_functions import count_message_words
from bot_functions import get_full_moon
from bot_functions import calculate
from bot_functions import play_cities
from bot_functions import load_cities


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


def main(token, proxy):
    mybot = Updater(token, request_kwargs=proxy)
    
    #create cities play function
    players = dict() 
    russian_cities = load_cities('russia_cities')
    random.shuffle(russian_cities)
    print(russian_cities)
    play_cities_part = functools.partial(play_cities, 
            cities_list = russian_cities, players = players)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", send_planet_constellation))
    dp.add_handler(CommandHandler("wordcount", count_message_words))
    dp.add_handler(CommandHandler("next_full_moon", get_full_moon))
    dp.add_handler(CommandHandler("calc", calculate))
    dp.add_handler(CommandHandler("cities", play_cities_part))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main(TOKEN,PROXY)
