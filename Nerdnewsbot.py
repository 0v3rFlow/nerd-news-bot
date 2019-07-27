# #!/usr/bin/python
# # -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------#
# Autore      : 0v3rFlow						       # 
# Descrizione : Telegramm bot per riceve le ultime news da 4 siti web:         #
#               Multiplayer.it, Tomshw.it, Spaziogames.it e Gamesvillage.it    #
# -----------------------------------------------------------------------------#

import time
import telepot
import urllib3
import re
import os
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop

multiplayer = 'https://multiplayer.it/'
tomshw = 'https://www.tomshw.it/ultimenews/24/'
spaziogames = 'https://www.spaziogames.it/pagina-news/'
gamesvillage = 'http://www.gamesvillage.it/category/videogiochi/videogiochi-news/'
const01 = 'Listening ...'
const02 = 200
const03 = 'article'
const04 = '/notizie/'
const05 = 'media media--standard'
const06 = 'https://api.telegram.org/bot'
const07 = '/sendMessage'
const08 = 'news_item_container_inner'
const09 = '(^https://|http://)'
const10 = 'post-title entry-header'

TOKEN = os.environ.get('API_TOKEN', None)
chat_id = os.environ.get('CHAT_ID', None)

urlbot = const06 + TOKEN + const07
ultime_news = {}


def on_chat_message(args):
    pass


def check_multiplayer(http, headers):
    # Faccio la richiesta al sito
    r = http.request('GET', multiplayer, headers=headers)
    if r.status == const02:
        # La nostra richiesta ha avuto esito positivo

        # Recuperiamo la risposta del server e utilizziamo soup per prendere l'html della pagina
        soup = BeautifulSoup(r.data, features="html.parser")

        # Estraggo solo il primo tag 'article'.
        article = soup.find(const03, attrs={'class': re.compile(const05)})

        # Estraggo il primo tag 'href' che trovo
        href = article.find('a', attrs={'href': re.compile(const04)})

        # Se notizie è vuoto, vuol dire che l'ultimo articolo che hanno pubblicato non fa parte della categoria "notizie"
        if href:

            # Controllo che non abbia già pubblicato la notizia
            news = href.get('href')

            # Controllo se ho già pubblicato l'articolo
            if news:
                print(ultime_news.get(1))
                if not news in ultime_news:
                    # Aggiorno il mio dizionario ed inivio la nuova news

                    # concatenazione del sito + l'href ricavato
                    link_sito = multiplayer + news

                    # Inserisco il sito nel mio dizionario così da fare il controllo il prossimo giro
                    ultime_news.update({1: link_sito})
                    print(link_sito)

                    return link_sito


def invia_messaggio(http, link_sito):
    # Invio il messaggio in chat
    r = http.request('POST', urlbot, fields={'chat_id': chat_id, 'text': link_sito})


def check_tomshw(http, headers):
    # Richiesta al sito
    r = http.request('GET', tomshw, headers=headers)
    if r.status == const02:
        # La nostra richiesta ha avuto esito positivo

        # Recuperiamo la risposta del server e utilizziamo soup per prendere l'html della pagina
        soup = BeautifulSoup(r.data, features="html.parser")

        # Estraggo il tag 'article'
        article = soup.find('article')

        # Estraggo il tag 'div' dentro 'article'
        row = article.find('div', attrs={'class': re.compile(const08)})

        # Estraggo il primo tag 'href' che trovo
        href = row.find('a', attrs={'href': re.compile(const09)})

        if href:
            news = href.get('href')

        if news:
            print(ultime_news.get(2))
            # Controllo se ho già pubblicato l'articolo

            if not news in ultime_news:

                # Aggiorno il mio dizionario ed inivio la nuova news
                ultime_news.update({2: news})
                print(news)

                return news


def check_spaziogames(http, headers):
    # Richiesta al sito
    r = http.request('GET', spaziogames, headers=headers)
    if r.status == const02:
        # La nostra richiesta ha avuto esito positivo

        # Recuperiamo la risposta del server e utilizziamo soup per prendere l'html della pagina
        soup = BeautifulSoup(r.data, features="html.parser")

        # Estraggo il tag 'h4'
        h4 = soup.find('h4')

        # Estraggo il primo tag 'href' che trovo
        href = h4.find('a', attrs={'href': re.compile(const09)})

        if href:
            # Estraggo il link
            news = href.get('href')

            if news:
                print(ultime_news.get(3))
                # Controllo se ho già pubblicato l'articolo
                if not news in ultime_news:
                    # Aggiorno il mio dizionario ed inivio la nuova news
                    ultime_news.update({3: news})
                    print(news)

                    return news


def check_gamevillage(http, headers):
    # Richiesta al sito
    r = http.request('GET', gamesvillage, headers=headers)
    if r.status == const02:
        # La nostra richiesta ha avuto esito positivo

        # Recuperiamo la risposta del server e utilizziamo soup per prendere l'html della pagina
        soup = BeautifulSoup(r.data, features="html.parser")

        # Estraggo il tag 'header'
        tagheader = soup.find('header', attrs={'class': re.compile(const10)})

        href = tagheader.find('a', attrs={'href': re.compile(const09)})

        if href:
            news = href.get('href')
            if news:
                print(ultime_news.get(4))
                # Controllo se ho già pubblicato l'articolo
                if not news in ultime_news:
                    # Aggiorno il mio dizionario ed inivio la nuova news
                    ultime_news.update({4: news})
                    print(news)
                    return news


def controlla_siti(http, chat_id):
    # Creo l'header per la get
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
    link_sito = ''

    # Multiplayer.com
    link_sito = check_multiplayer(http, headers)
    if link_sito:
        invia_messaggio(http, link_sito)

    # Tomshw.it
    link_sito = check_tomshw(http, headers)
    if link_sito:
        invia_messaggio(http, link_sito)

    # Spaziogames.it
    link_sito = check_spaziogames(http, headers)
    if link_sito:
        invia_messaggio(http, link_sito)

    # Gamesvillage.it
    link_sito = check_gamevillage(http, headers)
    if link_sito:
        invia_messaggio(http, link_sito)



if __name__ == "__main__":

    # Recuper il TOKEN
    bot = telepot.Bot(TOKEN)
    # Avvio il loop dei messaggi
    MessageLoop(bot, {'chat': on_chat_message, }).run_as_thread()
    http = urllib3.PoolManager()
    print(const01)
    while 1:
        controlla_siti(http, chat_id)
        time.sleep(840)

