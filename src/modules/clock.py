# -*- coding:utf-8 -*-
from datetime import datetime
from command import command

class clock(command):
    def __call__(self):
        today = datetime.today()
        clock = today.strftime("On est le %A %d %B, et il est a peu près %Hh%M")
        self.server.say('%s' % clock, self.channel)
