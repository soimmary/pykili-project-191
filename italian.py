import random
import matplotlib.pyplot as plt
import collections
import gspread
from oauth2client.service_account import ServiceAccountCredentials

WORDS_DICTIONARY = {}  # *ital_word*: *rus_word*
USERS = {}


def create_basis():
    """ создает базу слов из Google Sheets
    """
    global WORDS_DICTIONARY
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # NEW ________
    sheet = client.open('Italian Words')
    work_sheet = sheet.worksheet('parole')
    large_dictionary = {}

    row_max = work_sheet.row_count + 1
    for row in range(1, row_max):
        theme = work_sheet.row_values(row)[2]
        ital_word = work_sheet.row_values(row)[0]
        rus_word = work_sheet.row_values(row)[1]
        if theme not in large_dictionary:
            large_dictionary[theme] = {}
        large_dictionary[theme][ital_word] = rus_word

    WORDS_DICTIONARY = large_dictionary


def add_new_user(user_id):
    global USERS
    user_info = {'language': 'ital🇮🇹 -> rus🇷🇺',
                 'theme': 'il cibo 🍝',
                 'word_pair': None,
                 'forgotten_words': collections.Counter()}
    USERS[user_id] = user_info


def choose_word(user_id):
    """ спрашивает случайное слово из списка всех слов
    """
    theme = USERS[user_id]['theme']
    language = USERS[user_id]['language']
    USERS[user_id]['word_pair'] = random.choice(list(WORDS_DICTIONARY[theme].items()))
    if language == 'ital🇮🇹 -> rus🇷🇺':
        return USERS[user_id]['word_pair'][0]
    elif language == 'rus🇷🇺 -> ital🇮🇹':
        return USERS[user_id]['word_pair'][1]


def check_answer(user_id, answer):
    right_answer = ''
    language = USERS[user_id]['language']
    if language == 'ital🇮🇹 -> rus🇷🇺':
        right_answer = USERS[user_id]['word_pair'][1]
    elif language == 'rus🇷🇺 -> ital🇮🇹':
        right_answer = USERS[user_id]['word_pair'][0]
    if right_answer == answer:
        approval = ('Giusto☺️!', 'Bene🤓!', 'Correttamente🤩!', 'Essato☺️!',
                    'Certo🥰!', 'Bravo👏🏻!', 'Bravissima🥳!')
        return random.choice(approval)
    else:
        # какие итальянские слова часто забываешь
        USERS[user_id]['forgotten_words'][USERS[user_id]['word_pair'][0]] += 1
        return f'Ti sbagli ☹️:(\nLa risposta giusta: {right_answer}'


def drawing_bar(user_id):
    words = list(USERS[user_id]['forgotten_words'].values())
    number = list(USERS[user_id]['forgotten_words'].keys())

    plt.figure(figsize=(16, 9))
    plt.bar(number, words, color='pink')
    plt.title('Le parole che dimentichi')
    plt.ylabel('Volte')
    plt.xlabel('Parole')
    plt.savefig(r'grafico.png', bbox_inches=0)
 
