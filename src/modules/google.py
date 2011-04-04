# -*- coding:utf-8 -*-

from command import command

class google(command):
    def __call__(self):
        if self.message:
            self.server.say('http://www.google.com/search?q=%s' % self.message.replace(' ', '+'), self.channel)
        else:
            self.server.say('http://www.google.com', self.channel)
