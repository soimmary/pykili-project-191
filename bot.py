import telebot
import italian

TOKEN = '997358493:AAH2Hn57D3yFXgNh90lvQYrPzjPogVmIEqs'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])  # decorator
def start_message(message):
    bot.send_message(message.chat.id, 'CIAO!')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/ciao o ciao – damando la parola\n'
                                      '/sonostanco o sonostanco – \n'
                                      '/grafico - dimostro le parole in cui fai li sbagli spesso')


@bot.message_handler(commands=['ciao'])
def ciao_message_ask_language(message):
    keyboard_modello = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_modello.row('ital -> rus', 'rus -> ital')
    bot.send_message(message.chat.id, 'Scegli il modello', reply_markup=keyboard_modello)
    bot.register_next_step_handler(message, ciao_message_register_language)


def ciao_message_register_language(message):
    possible_answers = ('ital -> rus', 'rus -> ital')
    language = message.text.strip().lower()
    if language in possible_answers:
        ciao_message_ask(message, language)
    else:
        bot.send_message(message.chat.id, "L'errore")


def ciao_message_ask(message, language):
    if message.text.strip().lower() not in ('sonostanco', 'sono stanco'):  # proverka na ustalost'
        user_id = message.chat.id
        word = italian.choose_word()
        if language == 'ital -> rus':
            bot.send_message(message.chat.id, word[0])
        elif language == 'rus -> ital':
            bot.send_message(message.chat.id, word[1])
        bot.send_message(user_id, 'aspetto la tua risposta')
        bot.register_next_step_handler(message, ciao_message_check_answer, word=word)
    else:
        sonostanco_message(message)


def ciao_message_check_answer(message, word, language):
    answer = message.text.strip().lower()
    if answer not in ('sonostanco', 'sono stanco'):
        user_id = message.chat.id
        my_decision = italian.check_answer(answer, word, user_id)
        bot.send_message(user_id, my_decision)
        bot.register_next_step_handler(message, ciao_message_ask, language)
    else:
        sonostanco_message(message)


def sonostanco_message(message):
    bot.send_message(message.chat.id, 'hai lavorato bene!')


@bot.message_handler(content_types=['text'])
def ciao_text_message(message):
    if str(message.text).strip().lower() == 'ciao':
        ciao_message_ask_language(message)
    else:
        bot.send_message(message.chat.id, 'non so questo comando')


@bot.message_handler(commands=['grafico'])
def send_drawing_bar(message):
    italian.drawing_bar()
    bar = open('МАШУЛЯМОЛОДЕЦ.jpg', 'rb')
    bot.send_photo(message.chat.id, bar)


bot.polling(none_stop=True)
