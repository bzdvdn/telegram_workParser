import telebot
import os
import glob
from flask import Flask
from flask import request
import config as config
from workParser import workparse
from hhruParser import hhru_parse

__author__ = 'bzdvdn'



bot = telebot.TeleBot(config.token)
bot.remove_webhook()
bot.set_webhook(url='Your url')

print(bot.get_me())



def delete_file(filename):
	glb = glob.glob('./*.csv')
	os.remove(filename)


def work_parser(message,parser):
	if not message.text == '/start':		
		file = open(str(message.from_user.id) + '_-_' + str(message.text) + '.csv', 'rb')
		bot.send_message(message.from_user.id, 'parse done!')
		bot.send_document(message.from_user.id, file)
		delete_file(str(message.from_user.id)  + '_-_' + str(message.text) + '.csv')
	else:
		bot.register_next_step_handler(parser, start_command)




app = Flask(__name__)
app.config.from_object(config)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        update = telebot.types.Update.de_json(r)
        bot.process_new_updates([update])
        return ''

    return '<h1> Bot welcomes you</h1>'





@bot.message_handler(commands=['help'])
def handle_text(message):
	bot.send_message(message.chat.id, """
		Этот бот парсит сайты(work.ua, rabota.ua, hh.ru):
		на предмет поиска работы и выводит вам ссылку на спарсенный ресурс.
	команды /work_ua, /hh_ru, /rabota_ua
		после нажатия команд нееобходимо написать слово:
		по какому критерию вы хотите спарсить сайт. Например Python

		""")

@bot.message_handler(commands=['start'])
def start_command(message):
	#bot.send_message(message.chat.id, 'начинаем парсить!')
	user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	user_markup.row('/work_ua', '/hh_ru','/rabota_ua')
	user_markup.row('/help', '/stop')
	bot.send_message(message.from_user.id, 'Выберите команды для взаимодействия с ботом: ', reply_markup=user_markup)



@bot.message_handler(commands=['work_ua','hh_ru', 'rabota_ua'])
def work_ua_command(message):
	user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
	user_markup.row('python', 'ruby','php')
	user_markup.row('1с', 'front-end', '/start')
	bot.send_message(message.from_user.id, 'Выберите критерии для парсинга:', reply_markup=user_markup)
	if message.text == '/work_ua':
		@bot.message_handler(content_types=['text'])
		def handle_parser(message):
			bot.send_message(message.from_user.id, 'Waiting for parsing data...')	
			parser = workparse(message.text, message.from_user.id)
			work_parser(message,parser)
	elif message.text == '/hh_ru':
		@bot.message_handler(content_types=['text'])
		def handle_parser(message):
			bot.send_message(message.from_user.id, 'Waiting for parsing data...')	
			parser = hhru_parse(message.text, message.from_user.id)
			work_parser(message,parser)

	


@bot.message_handler(commands=['stop'])
def stop_command(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, 'конец взаимодействия с ботом: наберите "/start" для взаимодействия с ботом', reply_markup=hide_markup)



if __name__=='__main__':
    app.run()




#bot.polling(none_stop=True, interval=0)	