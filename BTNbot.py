import telebot
import requests
from config import TOKEN, API_KEY

bot = telebot.TeleBot(TOKEN)


symbol = 'BTCUSDT'
api_url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
#if response.status_code == requests.codes.ok:
    #print(response.json())
#else:
    #print("Error:", response.status_code, response.text)
    
data = response.json()
price = data['price']
price = float(price)
symbol = data['symbol']

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "this is a bot for BTCUSDT price")
    bot.register_next_step_handler(message, answer)
    
    
@bot.message_handler()
def answer(message):
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton(text='YES',
                                                    callback_data='yes')
    button_no = telebot.types.InlineKeyboardButton(text='No',
                                                   callback_data='no')
    keyboard.add(button_yes, button_no)
    
    bot.send_message(chat_id, f'Do you want to know BTCUSDT price?', reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def yes(call):
    message = call.message
    chat_id = message.chat.id
    bot.send_message(chat_id, f'{symbol}:  {price}$') 
@bot.callback_query_handler(func=lambda call: call.data == 'no')
def no(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.send_message(chat_id, 'жалко(')
    send_welcome(message)

if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()