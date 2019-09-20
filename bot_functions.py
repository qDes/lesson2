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
    except (IndexError, ValueError):
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
    '''Function gets quasinormal last char of word. '''
    bad_char = ['ъ','ь','й','ы']
    word = word[::-1]
    for char in word:
        if char not in bad_char:
            return char

def find_city(cities: list, player_cities: list, user_city: str) -> str:
    
    '''Function find city that was not in game.'''
    char = get_nonsoft_symbol(user_city).capitalize()
    for city in cities:
        if city[0] == char:
            if city in player_cities:
                continue
            return city

def reset_player(players, user_id):
    '''Procedure resets user profile data.'''
    players[user_id]['cities'] = []
    players[user_id]['last'] = ''


def validate_last_char(player, user_city):
    '''Function checks that last char from previous word
    equals first char of current word
    '''
    last_char_prev = player.get('last')
    if last_char_prev:
        if user_city[0].lower() != last_char_prev:
            return False
    return True

def validate_user_city(player, city, cities_list):
    '''Function checks that city was not in game and exists in cities_list''' 
    return (city not in player['cities']) and (city in cities_list)

def get_user_data(update):
    '''Function extracts user_id and user_city '''
    user_id = update.effective_user['id']
    try:
        user_city = update.message.text.split()[1]
    except IndexError:
        update.message.reply_text("Вы не ввели город. Попробуйте ещё.")
        user_city = ''
    return (user_id, user_city)

def update_player_profile(update,players,user_id, user_city, answer_city):
    '''Procedure adds to player's profile new cities and update last char '''
    players[user_id]['cities'].append(answer_city)
    players[user_id]['cities'].append(user_city)
    players[user_id]['last'] = get_nonsoft_symbol(answer_city)
    update.message.reply_text(f"{answer_city}. Ваш ход.")


def create_player(players, user_id):
    '''Procedure creates a player's profile if does not exist '''
    if players.get(user_id) == None:
        players[user_id] = {'cities':[], 'last':'' }
 

def play_cities(bot, update, cities_list, players):
    
    user_id, user_city = get_user_data(update)
    if not user_city:
        return None
    
    create_player(players, user_id)
    
    if not validate_last_char(players[user_id], user_city):
        reset_player(players, user_id)
        update.message.reply_text("Вы проиграли. Последняя буква не соответсвует первой. Начинаем заново")
        return None
    
    if not validate_user_city(players[user_id], user_city, cities_list):
        reset_player(players, user_id)
        update.message.reply_text("Вы проиграли. Город не валиден. Начинаем заново.")
        return None
    
    answer_city = find_city(cities_list,players[user_id]['cities'],user_city)
    if answer_city:
        update_player_profile(update, players, user_id, user_city, answer_city)
    else:
        update.message.reply_text("Вы выиграли.")
        reset_player(players, user_id)
        return None
