import telebot
import os
from flask import Flask
from flask import request
from flask_sslify import SSLify
import config as config
from Parser import Parser, HHruParser, RabotauaParser


__author__ = 'bzdvdn'



bot = telebot.TeleBot(config.token)

bot.remove_webhook()
bot.set_webhook(url='https://c5423e1f.ngrok.io')





app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object(config)

print(bot.get_me())

def delete_file(filename):
	os.remove(filename)

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
		на предмет поиска работы и выводит вам сsv файл.
	команды /work_ua, /hh_ru, /rabota_ua
		после нажатия команд нееобходимо выбрать слово из предложенных на клавиатуре:
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
	msg = bot.send_message(message.from_user.id, 'Выберите критерии для парсинга:', reply_markup=user_markup)
	
	if message.text == '/work_ua':
		bot.register_next_step_handler(msg, work_parser)
	elif message.text == '/hh_ru':
		bot.register_next_step_handler(msg, hh_parser)
	elif message.text == '/rabota_ua':
		bot.register_next_step_handler(msg, rabota_parser)
		


def work_parser(message):
	bot.send_message(message.from_user.id, 'Данные парсятся, это может занять некоторое время....')	
	p = Parser(url='https://www.work.ua/jobs-', page='page=',message=message.text, chat_id=message.from_user.id)			
	file = open(str(message.from_user.id) + '_-_' + str(message.text) + '.csv', 'rb')
	bot.send_document(message.from_user.id, file)
	delete_file(str(message.from_user.id)  + '_-_' + str(message.text) + '.csv')
	msg = bot.send_message(message.from_user.id, 'Готово! Для дальнейшей работы нажмите "/start"')


def hh_parser(message):
	bot.send_message(message.from_user.id, 'Данные парсятся, это может занять некоторое время....')	
	p = HHruParser(url='https://m.hh.ru/vacancies?text=', page='&page=', message=message.text, chat_id=message.from_user.id)		
	file = open(str(message.from_user.id) + '_-_' + str(message.text) + '.csv', 'rb')
	bot.send_document(message.from_user.id, file)
	delete_file(str(message.from_user.id)  + '_-_' + str(message.text) + '.csv')
	msg = bot.send_message(message.from_user.id, 'Готово! Для дальнейшей работы нажмите "/start"')

def rabota_parser(message):
	bot.send_message(message.from_user.id, 'Данные парсятся, это может занять некоторое время....')	
	p = RabotauaParser(url='https://rabota.ua/jobsearch/vacancy_list?keyWords=', page='&pg=', message=message.text, chat_id=message.from_user.id)			
	file = open(str(message.from_user.id) + '_-_' + str(message.text) + '.csv', 'rb')
	bot.send_document(message.from_user.id, file)
	delete_file(str(message.from_user.id)  + '_-_' + str(message.text) + '.csv')
	msg = bot.send_message(message.from_user.id, 'Готово! Для дальнейшей работы нажмите "/start"')






@bot.message_handler(commands=['stop'])
def stop_command(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.from_user.id, 'конец взаимодействия с ботом: наберите "/start" для взаимодействия с ботом', reply_markup=hide_markup)



if __name__=='__main__':
    app.run()




#bot.polling(none_stop=True, interval=0)	