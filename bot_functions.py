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
    char = word[-1].capitalize()
    if (char == 'Ь') or (char == 'Ъ'):
        char = word[-2].capitalize()
    return char

def find_city(cities: list, players_cities: list, user_city: str) -> str:
    
    char = get_nonsoft_symbol(user_city)
    for city in cities:
        if (city[0] == char) and (city not in players_cities):
            #print(3)
            return city
    return None



def play_cities(bot, update, cities_list, players):
    user_id = update.effective_user['id']
    try:
        user_city = update.message.text.split()[1]
        #print(user_city)
    except IndexError:
        update.message.reply_text("Ошибка. Попробуйте ещё.")

    if players.get('last'):
        if players.get('last') != user_city[0].lower():
            players[user_id] = []
            players['last'] = ''
            update.message.reply_text("You lose.")
            return None

        #if user_city[0].lower() != players.get('last'):
            #print('problem')
        #else:
            #print('no problem')
    if (user_city in cities_list) and (user_city not in players.get(user_id,[])):
        try:
            players[user_id].append(user_city)
        except KeyError:
            players[user_id] = [user_city]
    else:
        players[user_id] = []
        players['last'] = ''
        update.message.reply_text("You lose.")
        return None
    
    #print(2)
    answer_city = find_city(cities_list, players[user_id], user_city)
    if answer_city:
        players[user_id].append(answer_city)
        update.message.reply_text(f"{answer_city}. Your turn.")
        players['last'] = get_nonsoft_symbol(answer_city).lower()
        #print(last_char)
    else:
        players[user_id] = []
        update.message.reply_text("You won.")
    #print(answer_city)
    #print(players)
    #print('########')
    '''
    if user_city in all_cities:
        try:
            print(1)
            players_data[user_id].append(user_city)
        except KeyError:
            print(2)
            players_data[user_id] = [user_city]
    
    #check city existence
    if user_city not in all_cities:
        print(1)
        players_data['user_id'] = []
        update.message.reply_rext("Такого города нету. Играем заново.")
    #check city was in game
    elif user_city in players_data.get('user_id'):
        print(2)
        players_data['user_id'] = []
        update.message.reply_text("Такой город уже был. Играем заново.")
    else:
        print(3)
        try:
            players_data['user_id'].append(user_city)
        except KeyError:
            players_data['user_id'] = [user_city]
    
    print(4)
    #find city to answer
    last_char = user_city[-1].capitalize()
    print(last_char)
    print(players_data)
    save_players_data(players_data)
    ''' 

