# -*- coding: utf-8 -*-
import locale
import time
from signal import signal, SIGINT, SIGWINCH 

from simplebot import *
import settings
import __builtin__
from modules.news import *

def shut(signum, stackframe):
    print "YOO"



if __name__ == "__main__":
    signal(SIGINT, shut)
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')

    bot = FafaIrcBot2()

    if 'quakenet' in settings.servers.keys():
        __builtin__.botnews = news_t(bot.get_servers('quakenet'))
        botnews.start()
        # print 'DEBUG botnews start()'
