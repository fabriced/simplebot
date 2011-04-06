# -*- coding:utf-8 -*-

from lib.decorator import admin_required
from command import command
from lib.utils import  get_nick
from settings import *

class spam(command):

  @admin_required
  def do(self):
    if self.message:
      for chan in CHANNELS:
        if chan != self.channel:
        self.main.say('-spam- %s' % self.message, chan)
    else:
      self.main.say('Spam quoi, gros niais ?', get_nick(self.mask))
