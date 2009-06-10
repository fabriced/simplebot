# -*- coding : utf-8 -*- 

from command import command
from lib.utils import  get_nick
from lib.decorator import admin_required

class admin(command):
#TODO faire heriter de multiCommand, updater self.message ...

  @admin_required
  def do(self):
    if len(self.message.split(None, 2))>2:
      if self.message.split(' ', 2)[1] == "add":
        self.setAdmins(self.getAdmins().append(get_nick(self.message.split(' ', 2)[2]))
      if self.message.split(' ', 2)[1] == "rm":
        self.setAdmins(self.getAdmins().remove(get_nick(self.message.split(' ', 2)[2]))
    else:
      self.main.say(' !admin rm <nick> ou !admin add <nick> ?', get_nick(self.mask))
