import telebot
from telebot import types
from telebot import util
import re
import time
from time import sleep
import sys
import json
import os
import logging
import subprocess
import requests
import random
import base64
import urllib
from urllib import urlretrieve as dw
import urllib2
import redis
import requests as req
reload(sys)
sys.setdefaultencoding("utf-8")

TOKEN = '240545787:AAEwAOm2aKRcHVSYtLQ6gD-OBJFqCheA_OQ'
bot = telebot.TeleBot(TOKEN)
is_sudo = '232006008'
rediss = redis.StrictRedis(host='localhost', port=6379, db=0)

@bot.message_handler(commands=['start'])
def welcome(m):
    markup = types.InlineKeyboardMarkup()
    c = types.InlineKeyboardButton("About",callback_data='about')
    markup.add(c)
    b = types.InlineKeyboardButton("Help",callback_data='help')
    markup.add(b)
    oo = types.InlineKeyboardButton("Channel", url='https://telegram.me/CyberCH')
    markup.add(oo)
    id = m.from_user.id
    rediss.sadd('memberspy',id)
    bot.send_message("*HI\nSend Your PM*", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
     if call.message:
        if call.data == "help":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Send /help For See Help !")
     if call.message:
        if call.data == "about":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Soon ...")
     if call.message:
        if call.data == "text":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            bot.send_message(call.message.chat.id, '{}'.format(r))
	 if call.message:
        if call.data == "sticker":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_sticker(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "document":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_document(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "video":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_video(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "photo":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_photo(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "Audio":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_audio(call.message.chat.id, '{}'.format(r))
			
@bot.message_handler(commands=['stats'])
def send_stats(m):
    if m.from_user.id == 232006008:
        ban = str(rediss.scard('banlist'))
        usrs = str(rediss.scard('memberspy'))
        gps = str(rediss.scard('chats'))
        supergps = str(rediss.scard('supergroups'))
        text = '*Users* : *{}* \n\n*Groups* : *{}* \n\n*BanList* : *{}*'.format(usrs,gps,supergps,ban)
        bot.send_message(m.chat.id,text,parse_mode='Markdown')

@bot.message_handler(commands=['ban'])
def kick(m):
    if m.from_user.id == 232006008:
      if m.reply_to_message:
        ids = m.reply_to_message.from_user.id
        rediss.sadd('banlist',int(ids))
        bot.send_message(int(ids), '<b>You Are Banned!</b>',parse_mode='HTML')
        bot.send_message(m.chat.id, 'Banned!')

@bot.message_handler(commands=['unban'])
def send_stats(m):
    if m.from_user.id == 232006008:
      if m.reply_to_message:
        ids = m.reply_to_message.from_user.id
        rediss.srem('banlist',int(ids))
        bot.send_message(int(ids), '<b>You Are UnBanned!</b>',parse_mode='HTML')
        bot.send_message(m.chat.id, 'UnBanned!')

@bot.message_handler(content_types=['text','video','photo','sticker','document','audio','voice'])
def all(m):
        if m.chat.type == 'private':
            if m.text :
                fileid = m.photo[1]
			elif m.photo :
                fileid = m.photo[1]
            elif m.video :
                fileid = m.video
            elif m.sticker :
                fileid = m.sticker
            elif m.document :
                fileid = m.document
            elif m.audio :
                fileid = m.audio
            elif m.voice :
                fileid = m.voice
            e = m.from_user.username
            link = urllib2.Request("https://api.pwrtelegram.xyz/bot{}/getFile?file_id={}".format(TOKEN,fileid))
            open = urllib2.build_opener()
            f = open.open(link)
            link1 = f.read()
            jdat = json.loads(link1)
            patch = jdat['result']['file_path']
            send = 'https://storage.pwrtelegram.xyz/{}'.format(patch)
            bot.send_message(m.chat.id,'*File Id:*\n{}'.format(fileid),parse_mode='Markdown')
            bot.send_message(m.chat.id,'File Uploaded\nYour link: {}'.format(send))

@bot.message_handler(commands=['help'])
def clac(m):
    text = m.text.replace("/help","")
    bot.send_message(m.chat.id, "*List Of Commands :*\n\n/short URL\n_Shorten Your Link_\n/pic\n_Sned Random Picture_\n/tex Text\n_Take Sticker From Text_\n/kickme\n_Exit From Group_\n/id\n_Get Your ID_\n/me\n_Show Your Information_\n/food\n_Get Food Sticker_\n/mean Text\n_Get The Meaning Of Texts_\n/feedback Text\n_Send PM To Admin_\n/bold Text\n_Bold The Text_\n/italic Text\n_Italic The Text_\n/code Text\n_Code The Text_\n/echo Text\n_Echo The Text_\n/sticker (reply to photo)\n_Convert Photo To Sticker_\n/photo (reply to sticker)\n_Convert Sticker To Photo_\n/info\n_Get Your Information_\n/link\n_Get Group Link_\n/rank\n_Show Your Rank_\n/setsticker (reply to sticker)\n_Set Sticker For Your Self_\n/cap Text (reply to photo)\n_Write Text Under The Photo_\n/setphone PhoneNumber\n_Set Your PhoneNumber In The Bot_\n/myphone\n_Show Your PhoneNumber_\n\n*Get Users ID:*\nid (reply to message)\n\n*Uploader Panel:*\n_Send Your File In Private To Upload!_".format(text), parse_mode="Markdown")

bot.polling(True)
