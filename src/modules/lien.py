# -*- coding:utf-8 -*-

from command import command
from lib.decorator import devel

from settings import urls

class lien(command):

  def do(self):
    if self.message and urls.has_key(self.message.split()[0]):
      self.main.say(urls[self.message.split()[0]], self.channel)
