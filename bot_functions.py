import json
from datetime import datetime

import ephem

def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

def send_planet_constellation(bot, update):
    user_text= update.message.text
    #try to get planet name from text
    try:
        planet_name = user_text.split()[1].lower().capitalize()
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
    update.message.reply_text(f"Next fool moon on {full_moon_date}.")

def calculate(bot, update):
    user_text = update.message.text
    try:
        user_expression = user_text.split()[1]
        expression_result = eval(user_expression)
    except (SyntaxError, NameError, IndexError):
        update.message.reply_text("It is not math expression. Try another.")
    except ZeroDivisionError:
        update.message.reply_text('Zero division.')
    update.message.reply_text(str(expression_result))

def load_cities(cities):
    with open(cities, 'r') as file_read:
        cities = file_read.read()
        return json.loads(cities)


def get_nonsoft_symbol(word):
    char = word[-1]#.capitalize()
    if (char == 'ь') or (char == 'ъ'):
        char = word[-2]#.capitalize()
    return char

def find_city(cities: list, players_cities: list, user_city: str) -> str:
    
    char = get_nonsoft_symbol(user_city).capitalize()
    for city in cities:
        if (city[0] == char) and (city not in players_cities):
            #print(3)
            return city
    return None



def play_cities(bot, update, cities_list, players):
    '''{players: 'cities' : [], 'last': ''} '''
    user_id = update.effective_user['id']
    try:
        user_city = update.message.text.split()[1]
    except IndexError:
        update.message.reply_text("Ошибка. Попробуйте ещё.")
    #check player in players
    if players.get(user_id) == None:
        players[user_id] = dict()

    #check last char == first char of city 
    last_char = players[user_id].get('last')
    if last_char:
        if user_city[0].lower() != last_char:
            players[user_id]['cities'] = []
            players[user_id]['last'] = ''
            update.message.reply_text('Вы проиграли. Начинаем заново.')
            return None
    #check that user_city is valid and does not repeat
    if (user_city in cities_list) and (user_city not in players[user_id].get('cities',[])):
        #remeber user_city
        try:
            players[user_id]['cities'].append(user_city)
        except KeyError:
            players[user_id]['cities'] = []
    else:
        players[user_id]['cities'] = []
        players[user_id]['last'] = ''
        update.message.reply_text('Вы проиграли. Начинаем заново.')
        return None
    #finding city in cities_list    
    answer_city = find_city(cities_list, players[user_id]['cities'], user_city)
    if answer_city:
        players[user_id]['cities'].append(answer_city)
        update.message.reply_text(f"{answer_city}. Ваш ход.")
        players[user_id]['last'] = get_nonsoft_symbol(answer_city)
    else:
        players[user_id]['cities'] = []
        players[user_id]['last'] = ''
        update.message.reply_text('Вы выиграли.')

