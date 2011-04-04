# -*- coding:utf-8 -*-

#TODO improve displayed url

from command import command

class wiki(command):
    def __call__(self):
        if self.message:
            self.server.say('http://fr.wikipedia.org/wiki/Special:Recherche?search=%s' % self.message.replace(' ', '+'), self.channel)
        else:
            self.server.say('http://fr.wikipedia.org', self.channel)

