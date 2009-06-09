# -*- coding: utf-8 -*-
import locale
from simplebot import *


if __name__ == "__main__":
  locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
  bot = fafaIrcBot()
  bot.main_loop()
