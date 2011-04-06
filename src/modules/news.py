# -*- coding: utf-8 -*-

# !news // liste les news en mp
# !news start // démarre un thread
# !news stop // arrête un thread
# !news [name|url] // todo
# !news update // rafraichit manuellement le thread (useless ?)

from command import command
from settings import *
import main
import threading
import time
# from feedparser import parse
import lib.feedparser
from lib.decorator import admin_required
# from time import mktime
from datetime import datetime


class news(command):
    def __call__(self):
        self.message = self.message.split()
        print self.message
        if len(self.message) == 1:
            if self.message[0] == 'update':
                botnews.update_dict()
            elif self.message[0] == 'stop':
                self.cmdstart()
            elif self.message[0] == 'start':
                self.cmdstart()
            elif self.message[0] == '':
                # show all news
                botnews.show(None, None, user = self.user)
        elif len(self.message) == 0:
            # show all news
            botnews.show(None, None, user = self.user)

    @admin_required
    def cmdstart(self):
        if self.message[0] == 'start':
            botnews.paused = False
            # botnews.start()
            # botnews.run()
        elif self.message[0] == 'stop':
            botnews.paused = True
            # botnews.stop()

class news_t(threading.Thread):
    def __init__(self, server, timer = 2.0):
        threading.Thread.__init__(self)
        self.timer = timer
        self.server = server
        self.limit = 10
        self.current = 0
        self.active = True
        self.length = 5
        self.paused = False
        
        # init feeds
        f = open('./config/news.cfg', 'r')
        for line in f:
            if len(line) > 2:
                feed = line.strip().split('|')
                if len(feed) > 1:
                    self.news_dict[feed[0]] = feed[1]
                    # print 'FEED %s' % feed[0]
                    self.update_dict([feed[0],feed[1]], init = True)
                    if not self.channels_dict.get(feed[0]):
                        self.channels_dict[feed[0]] = []
                    for channel in feed[2:]:
                        if channel not in self.channels_dict.get(feed[0]):
                            self.channels_dict.get(feed[0]).append(channel)
        f.close
    def run(self):
        time.sleep(10.0)
        i = 0
        while self.active:
            if self.paused == False:
                # print 'DEBUG news_update:'
                for feedname, url in self.news_dict.iteritems():
                    # print 'DEBUG news: %s %s' % (feedname, url)
                    self.update_dict([feedname, url])
                # refresh tous les 1/4 d'heure
                time.sleep(15*60.0)
        print "DEBUG botnews: fin du thread"
    def stop(self):
        self.active = False
        # print 'DEBUG botnews: stop()'
    def update(self):
        # init feeds
        f = open('./config/news.cfg', 'r')
        for line in f:
            if len(line) > 2:
                feed = line.strip().split('|')
                if len(feed) == 2:
                    self.news_dict[feed[0]] = feed[1]
                    # print 'FEED %s' % feed[0]
                    self.update_dict([feed[0],feed[1]])
                    if not self.channels_dict.get(feed[0]):
                        self.channels_dict[feed[0]] = []
                    for channel in feed[2:]:
                        if channel not in self.channels_dict.get(feed[0]):
                            self.channels_dict.get(feed[0]).append(channel)
        f.close

    def show(self, timestamp, feed, user = None):
        if timestamp == None and feed == None:
            # recevoir en mp toutes les news en "mémoire" dans le bot
            for key, value in self.lastest_dict.iteritems():
                try:
                    # print '%s[%s] : %s - %s' % (value[0], time.strftime("%d %b %H:%M", time.localtime(key)), value[1], value[2])
                    # self.server.say(u'[%s] %s: %s - %s' % (value[0], time.strftime("%d %b %H:%M", time.localtime(key)), value[1], value[2]), user)
                    self.server.say(u'[%s] %s: %s - %s' % (value[0], datetime.fromtimestamp(mktime(item.updated_parsed)), value[1], value[2]), user)
                except:
                    # print u'WARNING %s[%s] : %s - %s' % (value[0], time.strftime("%d %b %H:%M", time.localtime(key)), value[1], value[2])
                    print "WARNING: encodage qui foire ?"
        else:
            # afficher une "nouvelle" news dans tous les channels concernés
            # appel interne par update_dict
            for channel in self.channels_dict.get(feed[0]):
                try:
                    # print '!NEWS %s[%s] : %s - %s' % (feed[0], time.strftime("%d %b %H:%M", time.localtime(timestamp)), feed[1], feed[2])
                    # self.server.say(u'[%s] !NEWS %s: %s - %s' % (feed[0], time.strftime("%d %b %H:%M", time.localtime(timestamp)), feed[1], feed[2]), channel)
                    # self.server.say(u'\x034[%s] %s:\x03 %s - %s' % (feed[0], time.strftime("%d %b %H:%M", time.localtime(timestamp)), feed[1], feed[2]), channel)
                    self.server.say(u'\x034[%s] %s:\x03 %s - %s' % (feed[0], datetime.fromtimestamp(mktime(item.updated_parsed)), feed[1], feed[2]), channel)
                except:
                    print "WARNING: encodage qui foire ?"
    def update_dict(self, feed, init = False):
        try:
            myfeed = parse(feed[1])
            # trouver le plus petit timestamp
            min_dict = None
            for lastest in self.lastest_dict.iterkeys():
                if min_dict == None or lastest < min_dict:
                    min_dict = lastest
            
            # parcours chaque item du flux
            for item in myfeed['entries']:
                # print item
                # print '%s[%s] : %s - %s' % (feed[0], item.updated, item.title, item.links[0].get('href'))
                # Tue, 29 Mar 2011 15:11:06 +0000
                # format = '%a, %d %b %Y %H:%M:%S %z'
                # item.timestamp = time.mktime(time.strptime(item.updated, format))
                if item.updated_parsed != None:
                    item.timestamp = time.mktime(item.updated_parsed)
                elif feed[0] == 'qw.nu': 
                    # 'updated': u'29 Mar 2011 @ 11:02'
                    locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
                    format = '%d %b %Y @ %H:%M'
                    locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
                    item.timestamp = time.mktime(time.strptime(item.updated, format))
                    # item.timestamp = time.mktime(item.updated_parsed)
                else:
                    item.timestamp = int(time.time())


                if item.timestamp in self.lastest_dict and self.lastest_dict.get(item.timestamp)[1] == item.title and self.lastest_dict.get(item.timestamp)[2] == item.links[0].get('href'):
                    # print 'DEBUG allready IN %s' % item.links[0].get('href')
                    added = False
                else:
                    # print 'timestamp: %s' % item.timestamp
                    # print 'DEBUG news: DICT %s' % str(self.lastest_dict)
                    added = False
                    if len(self.lastest_dict) <= self.length:
                        self.lastest_dict[item.timestamp] = [feed[0], item.title, item.links[0].get('href')]
                        added = True
                    else:
                        # print "%s : TIMESTAMP %s ; MIN_DICT %s" % (item.title, str(item.timestamp), str(min_dict))
                        if item.timestamp > min_dict: # or min_dict == None:
                            # if min_dict != None:
                            del self.lastest_dict[min_dict]
                            self.lastest_dict[item.timestamp] = [feed[0], item.title, item.links[0].get('href')]
                            added = True
                            
                    if added == True:
                        if init == False:
                            self.show(item.timestamp, self.lastest_dict.get(item.timestamp))
                        min_dict = None
                        for lastest in self.lastest_dict.iterkeys():
                            if min_dict == None or lastest < min_dict:
                                min_dict = lastest
        except:
            print "DEBUG BUG update_"
        # print 'DEBUG news: DICT: %s' % self.lastest_dict


# FFF [23 mars 18:30] : http://url.com - title
# {'name1':'url1', 'name2':'url2'}
news_t.news_dict = {}
# {timestamp1:['name1','title1','url1'], timestamp2:['name2','title2','url2']}
news_t.lastest_dict = {}
# {'name1':['chan1','chan2'], 'name2':['chan1','chan2','chan3']}
news_t.channels_dict = {}



