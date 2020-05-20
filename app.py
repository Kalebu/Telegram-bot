import time 
import json
import telepot
import random
import schedule
import wikiquote
from telepot.loop import MessageLoop
from difflib import get_close_matches

bot = telepot.Bot('your-telegram-key')
Knowledge = json.load(open('knowledge.json'))

greeting = ['hi', 'hello', 'niaje', 'mambo']
sending  = ['nitumie', 'send me ', 'send', 'tuma']
define = ['define', 'maana', 'meaning']
picture = ['picha', 'picture', 'pic']
audio = ['audio', 'mp3', 'music']
video = ['video', 'movie']
document = ['document', 'file', 'fail']
sending_picture = set(sending+picture)
sending_audio = set(sending+audio)
sending_video = set(sending+video)
sending_document = set(sending+document)

Topic = ['life', 'love', 'money', 'jesus']

active_user_id = []

def random_quote():
    random_topic = random.choice(Topic)
    quotes = wikiquote.quotes(random_topic)
    quote = random.choice(quotes)
    return quote 

def check_new(message):
    user_id = message['chat']['id']
    user_firstname = message['chat']['first_name']
    user_lastname = message['chat']['last_name']
    full_name = user_firstname + ' ' + user_lastname
    user_message = message['text']
    
    if user_id not in active_user_id:
        active_user_id.append(user_id)

    if user_message in greeting:
        greet = random.choice(greeting)
        reply =  greet + '\n' + full_name
        bot.sendMessage(user_id, reply) 
    else:
        message_list = user_message.split(' ')
        Message_list = set(message_list)
        if len(message_list) == 1 or 'define' in user_message :
            close_match = get_close_matches(message_list[-1], Knowledge.keys())
            if close_match:
                reply = Knowledge[close_match[0]][0]
                bot.sendMessage(user_id,  reply)
            else:
                reply = 'Can\'t find answer to your response'
                bot.sendMessage(user_id, reply)
     

        elif len(Message_list.intersection(sending_picture))>1:
            bot.sendPhoto(user_id, photo=open('picture.png', 'rb'))

        elif len(Message_list.intersection(sending_audio))>1:
            bot.sendAudio(user_id, audio = open('fracture.mp3', 'rb'))

        elif len(Message_list.intersection(sending_video))>1:
            bot.sendVideo(user_id, video = open('cars.mp4', 'rb'))

        elif len(Message_list.intersection(sending_document))>1:
            bot.sendDocument(user_id, document =open('knowledge.json', 'rb'))

        else:
            reply = 'Sorry didn\'t understand it \n can you rephrase it in another short way'
            bot.sendMessage(user_id, reply)       
        
def sending_message():
    for user in active_user_id:
        quote = random_quote()
        bot.sendMessage(user, quote)        

MessageLoop(bot, check_new).run_as_thread()

while True:
    time.sleep(10)
    sending_message()