# -*- coding: utf-8 -*-
import locale
from simplebot import *


if __name__ == "__main__":
  locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
  bot = fafaIrcBot()
  if bot.get_modpath() == "":
    print "ERROR : You need to set MODPATH in settings.py"
  else:
    bot.main_loop()
