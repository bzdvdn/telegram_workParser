import telebot
import os
import glob
import config
from datetime import datetime
from workParser import workparse
from hhruParser import hhru_parse

__author__ = 'bzdvdn'

token = config.token
# print(token)

bot = telebot.TeleBot(token)

# bot.send_message(394828462, 'Hello')

# upd = bot.get_updates()
# print(upd)

# last_upd = upd[-1]
# message_from_user = last_upd.message
# print(message_from_user)
print(bot.get_me())

# def log(message, answer):
# 	print('\n'+ '='*8)
# 	print(datetime.now())
# 	print("Сообщение от {0} {1}. (id = {2}) \n Текст = {3}".format(message.from_user.first_name,
# 															       message.from_user.last_name,
# 															       str(message.from_user.id),
# 															       message.text))
# 	print(answer)

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







bot.polling(none_stop=True, interval=0)	