from creds import *
import msgtext
import grabTimepad as tpad

import telebot
from telebot import types

import datetime
from babel.dates import format_datetime


bot = telebot.TeleBot(API_TG_TOKEN, parse_mode=None) 


eventsList = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	print_msg_in_console(message)
	markup = types.ReplyKeyboardMarkup()
	itembtn = types.KeyboardButton('/tickets')
	markup.add(itembtn)
	bot.reply_to(message, msgtext.hello, reply_markup=markup)


@bot.message_handler(commands=['orders', 'tickets'])
def send_orders(message):
	print_msg_in_console(message)
	global eventsList
	eventsList = tpad.get_datesNames(tpad.get_events(tpad.orgIdKiosk))

	markup = types.InlineKeyboardMarkup()
	for key in eventsList.keys():
		human_date = format_datetime(eventsList[key][1], locale='ru_RU')
		callback_data = key
		itembtn = types.InlineKeyboardButton(human_date)
		itembtn.callback_data = callback_data
		markup.add(itembtn)

	if eventsList == {}:
		bot.send_message(message.chat.id, msgtext.empty_list)
	elif len(eventsList)==1:
		event_id = str(list(eventsList.keys())[0])
		message_body = form_orders_msgbody(event_id)
		bot.send_message(message.chat.id, message_body)
	else: 
		bot.send_message(message.chat.id, msgtext.choose_event , reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
	event_id = call.data
	message_body = form_orders_msgbody(event_id)

	print_name = call.from_user.first_name
	print_username = call.from_user.username
	date = datetime.datetime.today()
	human_date = format_datetime(date, locale='ru_RU')
	print_msg = f'{human_date}: ANSWER2: {print_name} -- [@{print_username}]: !{message_body}!'
	print(print_msg)

	bot.answer_callback_query(call.id)
	bot.send_message(call.message.chat.id, message_body)


@bot.message_handler(func=lambda m: True)
def spam(message):
	print_msg_in_console(message)



def form_orders_msgbody(event_id):
	# event id comes in str
	orders = tpad.get_orders(event_id)
	
	global eventsList
	event_name = eventsList[int(event_id)][0]

	dlc = ''
	if orders[0] == 0:
		dlc = f'\n{msgtext.joke_on_popularity}'

	message_body = f'{event_name}\n{msgtext.orders} {orders[0]}, {msgtext.tickets}: {orders[1]} {dlc}'
	return message_body


def print_msg_in_console(message):
	date = message.date
	date = datetime.datetime.fromtimestamp(date)
	human_date = format_datetime(date, locale='ru_RU')

	first_name = message.from_user.first_name
	username = message.from_user.username
	msg_text = message.text
	print_msg = f'{human_date}. {first_name} [@{username}]: {msg_text}'
	print(print_msg)



bot.infinity_polling()