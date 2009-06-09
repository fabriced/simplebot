# -*- coding:utf-8 -*-
from datetime import datetime
from command import command

class clock(command):
  def do(self):
    today = datetime.today()
    clock = today.strftime("On est le %A %d %B, et il est a peu près %Hh%M")
    self.main.say('%s' % clock, self.channel)
