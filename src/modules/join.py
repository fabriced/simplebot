#coding -*- utf-8 -*-

from command import command

from lib.decorator import admin_required

class join(command):

  def do(self):
    if self.message.split()[1:]:
      main.s.send("JOIN %s\n" % self.message.split()[1])
