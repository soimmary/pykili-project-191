import telebot
from telebot.types import KeyboardButton
import italian
import os

# подключение к боту
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
# создание базы слов
italian.create_basis()


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in italian.USERS:
        italian.add_new_user(message.chat.id)
    bot.send_message(message.chat.id, 'Ciao🤩!')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/ciao – damandare la parola\n'
                                      'sono stanca o sono stanco – finire di praticare\n'
                                      '/grafico - dimostrare le parole in cui fai gli sbagli spesso')


@bot.message_handler(commands=['ciao'])
def ciao_message_ask_theme(message):
    if message.chat.id not in italian.USERS:
        italian.add_new_user(message.chat.id)
    keyboard_theme = telebot.types.ReplyKeyboardMarkup(True, True)
    themes = tuple(italian.WORDS_DICTIONARY.keys())
    for i in range(0, len(themes), 2):
        left = KeyboardButton(themes[i])
        try:
            right = KeyboardButton(themes[i+1])
            keyboard_theme.add(left, right)
        except IndexError:
            keyboard_theme.add(left)
            break
    bot.send_message(message.chat.id, 'Scegli il tema', reply_markup=keyboard_theme)
    bot.register_next_step_handler(message, ciao_message_register_theme)


def ciao_message_register_theme(message):
    possible_answers = tuple(italian.WORDS_DICTIONARY.keys())
    theme = message.text.strip().lower()
    if theme in possible_answers:
        italian.USERS[message.chat.id]['theme'] = theme
        ciao_message_ask_language(message)
    else:
        bot.send_message(message.chat.id, "L'errore❗️")


def ciao_message_ask_language(message):
    keyboard_modello = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_modello.row('ital🇮🇹 -> rus🇷🇺', 'rus🇷🇺 -> ital🇮🇹')
    bot.send_message(message.chat.id, 'Scegli il modello', reply_markup=keyboard_modello)
    bot.register_next_step_handler(message, ciao_message_register_language)


def ciao_message_register_language(message):
    possible_answers = ('ital🇮🇹 -> rus🇷🇺', 'rus🇷🇺 -> ital🇮🇹')
    language = message.text.strip().lower()
    if language in possible_answers:
        italian.USERS[message.chat.id]['language'] = language
        ciao_message_ask(message)
    else:
        bot.send_message(message.chat.id, "L'errore❗️")


def ciao_message_ask(message):
    answer = message.text.strip().lower()
    if answer not in ('sono stanca', 'sono stanco'):  # proverka na ustalost'
        word = italian.choose_word(message.chat.id)
        bot.send_message(message.chat.id, word)
        bot.send_message(message.chat.id, 'Aspetto la tua risposta ⏰')
        bot.register_next_step_handler(message, ciao_message_check_answer)
    else:
        sonostanca_message(message)


def ciao_message_check_answer(message):
    answer = message.text.strip().lower()
    if answer not in ('sono stanca', 'sono stanco'):
        my_decision = italian.check_answer(message.chat.id, answer)
        bot.send_message(message.chat.id, my_decision)
        ciao_message_ask(message)
    else:
        sonostanca_message(message)


def sonostanca_message(message):
    bot.send_message(message.chat.id, 'Hai lavorato bene 🤗!')


@bot.message_handler(commands=['grafico'])
def send_drawing_bar(message):
    if message.chat.id not in italian.USERS:
        italian.add_new_user(message.chat.id)
    italian.drawing_bar(message.chat.id)
    bar = open('grafico.png', 'rb')
    bot.send_photo(message.chat.id, photo=bar)


@bot.message_handler(commands=['update'])
def update_message(message):
    italian.create_basis()
    bot.send_message(message.chat.id, 'obnovleno')


@bot.message_handler(content_types=['text'])
def ciao_text_message(message):
    if str(message.text).strip().lower() == 'ciao':
        ciao_message_ask_theme(message)
    else:
        bot.send_message(message.chat.id, 'Non so questo comando ☹️')


bot.polling(none_stop=True)
