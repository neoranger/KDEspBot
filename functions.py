# -*- coding: utf-8 -*-
import telebot # Library of API bot.
from telebot import types # Types from API bot
import codecs
import sys
from os.path import exists
import os
import token
import user
import feedparser
import owners
import logging
import commands
import subprocess
import requests

TOKEN = token.token_id
bot = telebot.TeleBot(TOKEN) # Creating our bot object.
bot.skip_pending=True

#######################################
#Function for feedparser
#CODE TAKEN FROM:
#https://gist.github.com/Jeshwanth/99cf05f4477ab0161349
def get_feed(url):
    try:
        feed = feedparser.parse(url)
    except:
        return 'Invalid url.'
    y = len(feed[ "items" ])
    y = 5 if y > 5 else y
    if(y < 1):
        return 'Nothing found'
    lines = ['*Feed:*']
    for x in range(y):
        lines.append('- [{}]({})'.format(feed['items'][x]['title'].replace(']', ':').replace('[', '').encode('utf-8'), feed['items'][x]['link']))
    return '\n'.join(lines)
#    for x in range(y):
#        lines.append(
#        u'-&gt <a href="{1}">{0}</a>.'.format(
#        u'' + feed[ "items" ][x][ "title" ],
#        u'' + feed[ "items" ][x][ "link" ]))
#    return u'' + '\n'.join(lines)

#######################################

#Functions
@bot.message_handler(content_types=['new_chat_member'])
def command_new_user(m):
    cid = m.chat.id
    grupo = m.chat.title
    if (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + '!! ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'No tenés nombres, podrías completar los datos. Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + '!!' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.last_name) + '!!' + ' A.K.A. ' + '@' + str(m.new_chat_member.username) + ' a ' + unicode(grupo) + '. ' + 'Te sugerimos leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' A ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.last_name) + '!! ' + ' a ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, 'Bienvenido' + ' ' + unicode(m.new_chat_member.first_name) + '!! ' + ' a ' + grupo + '. ' + 'No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en #Normas.')

@bot.message_handler(content_types=['left_chat_member'])
def command_left_user(m):
    cid = m.chat.id
    bot.send_message(cid, '@' + unicode(m.left_chat_member.username) + ' Gracias por pasar!! Bye!! ')

@bot.message_handler(commands=['help'])
def command_ayuda(m):
    cid = m.chat.id
    bot.send_message( cid, "Comandos Disponibles:\n /blog\n /neofeed\n /manjarofeed\n /kdefeed\n /id\n /mirrors\n /keys\n /update\n /orphans\n /listpkg\n /last_update_changes\n /virtualbox\n /youtubedl\n /mpis\n /github\n /about\n /support\n /isos\n /help\n") #

@bot.message_handler(commands=['about'])
def command_about(m):
    cid = m.chat.id
    bot.send_message( cid, 'Acerca de @KDEspBot: Creado por NeoRanger - www.neositelinux.com')

@bot.message_handler(commands=['support'])
def command_support(m):
    markup = types.InlineKeyboardMarkup()
    itembtnneo = types.InlineKeyboardButton('NeoRanger', url="telegram.me/NeoRanger")
    itembtnblog = types.InlineKeyboardButton('URL Blog', url="http://www.neositelinux.com")
    itembtnrepo = types.InlineKeyboardButton('Repo Github', url="https://github.com/neoranger/KDEspBot")
    markup.row(itembtnneo)
    markup.row(itembtnblog)
    markup.row(itembtnrepo)
    bot.send_message(m.chat.id, "Choose an option:", reply_markup=markup)


#@bot.message_handler(commands=['blog'])
#def command_blog(m):
#    cid = m.chat.id
#    busqueda = 'URL HERE'    
#    if len(m.text.split()) >= 2:
#        palabras = m.text.split()
#        palabras.pop(0)
#        a_buscar = '+'.join(palabras)
#        url = (busqueda % a_buscar)
#        bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")
#    else:
#        bot.send_message( cid, "Missing Argument" )

@bot.message_handler(commands=['feed'])
def command_feed(m):
    cid = m.chat.id
    url = str(m.text).split(None,1)
    print (url)
    bot.send_message(cid, get_feed(url[1]),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['kdefeed'])
def kde_feed(m):
    cid = m.chat.id
    url = str("https://www.kdeblog.com/feed/")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

###############################################################################
#Specials functions
def send_message_checking_permission(m, response):
    cid = m.chat.id
    uid = m.from_user.id
    if uid != user.user_id:
        bot.send_message(cid, "You can't use the bot")
        return
    bot.send_message(cid, response)

###############################################################################
print('Functions loaded')
