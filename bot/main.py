import requests
import telebot
from config import TELEGRAM_BOT_TOKEN, JWT_SECRET_KEY, API_URL
import jwt

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	try:
		token = message.text.split(' ')[1]
	except Exception as e:
		print(e)
		return

	if message.from_user.username:
		username = message.from_user.username
	else:
		username = message.from_user.first_name

	payload = {
		'token': token,
		'user_id': message.from_user.id,
		'username': username
	}
	encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
	res = requests.post(API_URL + '/register_user/', json={'token': encoded_jwt})
	print(res.text)
	bot.reply_to(message, 'You authorized')


if __name__ == '__main__':
	bot.infinity_polling()