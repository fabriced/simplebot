# -*- coding:utf-8 -*-

from command import command
from lib.decorator import admin_required

class mode(command):

  @admin_required
  def do(self):
    phrase = " ".join(self.message.split()[1:])
    self.main.send('MODE %s\n' %  phrase) 
