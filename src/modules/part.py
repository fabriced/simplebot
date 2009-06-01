# -*- coding : utf-8 -*- 

from command import command

from lib.decorator import admin_required

class part(command):

  @admin_required
  def do(self):
    self.main.s.send("PART %s\n" % self.message.split()[1])
