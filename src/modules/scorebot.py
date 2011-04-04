# -*- coding: utf-8 -*-

# !scorebot <game> <ip> [start] // facultatif
# !scorebot [stop] <ip> [stop]
# !scorebot [status] <ip> [status]

from command import command
from lib.decorator import admin_required
import threading
import time
from lib.pyquake import *

class scorebot(command):
    def __call__(self):
        self.message = self.message.split()
        
        action = None
        
        if len(self.message) == 2:
            if self.message[0] in ['qw', 'q3', 'pk']:
                # cas !scorebot <game> <ip> [start]
                action = 'start'
                game = self.message[0]
                ip = self.message[1]
            else:
                # cas !scorebot [stop] <ip> [stop]
                # cas !scorebot [status] <ip> [status]
                if self.message[0] in ['stop', 'status']:
                    action = self.message[0]
                    ip = self.message[1]
                elif self.message[1] in ['stop', 'status']:
                    ip = self.message[0]
                    action = self.message[1]
        
        if action == 'status':
            if ip in self.scorebot_dict:
                print 'DEBUG scorebot: status %s' % ip
                self.server.say(self.scorebot_dict.get(ip).status(), self.channel)
        elif action == 'stop':
            if ip in self.scorebot_dict:
                print 'DEBUG scorebot: stop %s' % ip
                self.scorebot_dict.get(ip).stop()
                self.server.say(self.scorebot_dict.get(ip).status(), self.channel)
        elif action == 'start':
            if ip not in self.scorebot_dict:
                print 'DEBUG scorebot: start %s' % ip
                scorebot = scorebot_t(ip, game)
                scorebot.start()
                self.scorebot_dict[ip] = scorebot
                
class scorebot_t(threading.Thread):
    def __init__(self, name = '', game = '', timer = 2.0):
        threading.Thread.__init__(self)
        self.name = name
        self.game = game
        self.timer = timer
        self.limit = 10
        self.current = 0
        self.active = True
    def run(self):
        i = 0
        while self.active:
            print 'DEBUG scorebot: update_score:'
            self.getscore()
            time.sleep(10.0)
        print "DEBUG scorebot %s arrêté" % self.nom
    def status(self):
        if self.active == True:
            return 'Scorebot demarré'
        else:
            return 'Scorebot arrêté'
    def stop(self):
        self.active = False
    def getscore(self):
        # self._timer = threading.Timer(tempo, self.score)
        if self.game == 'qw':
                g = PyQuakeWorld(self.name, rcon_password='')
        if self.game == 'q3':
                g = PyQuake3(self.name, rcon_password='')
        if self.game == 'pk':
                g = PyPainkiller(self.name, rcon_password='')
        g.update()
        print g
        """if self.current == 0:
            print 'DEBUT DU MATCH %s' % (self.nom)
            print 'Temps restant (%s) : %s' % (self.nom, str(self.limit))
        elif self.current < self.limit:
            print 'Temps restant (%s) : %s' % (self.nom, str(self.limit-self.current))
        else:
            print 'FIN DU MATCH %s' % (self.nom)
            self.stop()
        self.current = self.current + 1"""
        

# scorebot.scorebot_dict = {'ip1':'thread1','ip2':'thread2'}
scorebot.scorebot_dict = {}

print 'FIN'


