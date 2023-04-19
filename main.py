from pyobigram.client import *
from pyobigram.inline import *

import tioanime


BOT_TOKEN = '6008460161:AAGfyLa6ZXiXdD35PRuAowbB3IJFwJl3Y6Y'


def search_handle(update,bot:ObigramClient):

    query = update.inline_query.query
    results = []

    if query!='':
        named = True
        try:
            index = int(query)
            named = False
        except:pass
        epis = tioanime.search(query,named)
        id = 0
        for ep in epis:
            name = ep["Anime"]
            doc = inlineQueryResultDocument(id, title=name, text=f'/tanime {name}', thumb_url=ep['Image'])
            results.append(doc)
            id += 1
    else:
        epis = tioanime.get_latest_episodies()
        id = 0
        for ep in epis:
            name = ep["Anime"]
            doc = inlineQueryResultDocument(id,title=name,text=f'/taepi {name}',thumb_url=ep['Image'])
            results.append(doc)
            id += 1

    bot.answer_inline(update.inline_query.id,results)
    pass

def message_handle(update,bot:ObigramClient):
    text = ''
    try:
        message = update.message
        text = message.text
    except:pass

    if '/start' in text:
        msg_text = '✨Bienvenido @{0} a nuestro bot TASearch , Buscador de animes en telegram, Mantente al día del progeso del proyecto en este Canal✨'
        msg_text = msg_text.replace('{0}',message.chat.username)
        reply_markup = inlineKeyboardMarkup(r1=[
            inlineKeyboardButton('✨Download Service By @JosePC98✨',url='https://t.me/DL_Service_Jose_PC98')
        ])
        bot.send_message(message.chat.id,msg_text,reply_markup=reply_markup,reply_to_message_id=message.message_id)

    if '/tanime' in text:
        name = str(text).replace('/tanime ', '')
        animes = tioanime.search(name)
        anime = None
        for a in animes:
            if a['Anime'] == name:
                anime = a
                break
        caps = tioanime.get_info(anime['Url'])
        html = '<a href="' + anime['Image'] + '">' + anime['Anime'] + '</a>\n'
        html += '<b>Sinopsis:</b>\n' + caps['sinopsis'] + '\n\n'
        html += '<b>Capitulos:</b>' + str(len(caps['episodies']))
        buttons = []
        index = 0
        capit = 1
        max = 2
        list = []
        for cap in caps['episodies']:
            try:
                mega = tioanime.get_mega_url(cap)
                list.append(inlineKeyboardButton(text='Capitulo ' + str(capit), url=mega))
            except Exception as ex:
                pass
            if index>=max-1:
                buttons.append(list)
                index = 0
                list = []
            index += 1
            capit += 1
        buttons.append(list)
        bot.send_message(message.chat.id,html, parse_mode='HTML', reply_markup=inlineKeyboardMarkupArray(buttons),reply_to_message_id=message.message_id)

    if '/taepi' in text:
        name = str(text).replace('/taepi ', '')
        epis = tioanime.get_latest_episodies()
        epi = None
        for ep in epis:
            if ep['Anime'] == name:
                epi = ep
                break
        if epi:
            megaurl = tioanime.get_mega_url(epi['Url'])
            html = '<a href="' + epi['Image'] + '">' + epi['Anime'] + '</a>'
            bot.send_message(message.chat.id,html, parse_mode='HTML', reply_markup=inlineKeyboardMarkup(r1=[
                inlineKeyboardButton(text='Mega Url', url=megaurl)
            ]),reply_to_message_id=message.message_id)

    pass


if __name__ == '__main__':
    bot:ObigramClient = ObigramClient(BOT_TOKEN)
    bot.onMessage(message_handle)
    bot.onInline(search_handle)
    print('bot runing!')
    bot.run()


