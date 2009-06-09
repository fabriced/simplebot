# -*- coding:utf-8 -*-

from command import command
from lib.decorator import admin_required

class mode(command):

  @admin_required
  def do(self):
    self.main.send('MODE %s\n' % self.message) 
