# -*- coding: utf-8 -*-
# http://abcdrfc.free.fr/rfc-vf/rfc1459.html#41

import sys
import socket
import string
import imp, inspect
import glob, os
import re
import time

from settings import *
from lib.exception import *
from threading import Event, Thread

import settings

def get_mod_func(callback):
    # Converts 'django.views.news.stories.story_detail' to
    # ['django.views.news.stories', 'story_detail']
    try:
        dot = callback.rindex('.')
    except ValueError:
        return callback, ''
    return callback[:dot], callback[dot+1:]

class FafaIrcBot2(object):
    
    _servers = {}
    _handlers = {}

    def __init__(self):
        super(FafaIrcBot2, self).__init__()
        for dirname, dirnames, filenames in os.walk('./modules'):
            for filename in filenames:
                # print 'DEBUG FafaIrcBot2 %s' % filename
                if filename[-3:] == '.py':# and filename != 'news.py':
                    # mod = str(filename[:-3])
                    # path = str(dirname[2:]+'.'+filename[:-3]+'.'+filename[:-3])
                    self.register_handler(filename[:-3], '%s.%s.%s' % (dirname[2:], filename[:-3], filename[:-3]))
        # alias
        self.register_handler('add', 'modules.ech.ech')
        self.register_handler('clear', 'modules.ech.ech')
        self.register_handler('list', 'modules.ech.ech')
        self.register_handler('ready', 'modules.ech.ech')
        self.register_handler('rm', 'modules.ech.ech')

        for id, infos in settings.servers.items():
            self._servers[id] = ServerConnection(self, id, **infos)
            self._servers[id].start()

    def register_handler(self, cmd, callback):
        # c'est bien beau ca, mais comment on appele cette methode ?
        # here is the solution, il faut 2 mecanismes:
        # pouvoir avoir des commandes auto lancées (un genre de build-in qui reste modulaire)
        # faire une commande buildin qui permette d'enregistrer les cmd

        # GRUIIIIIIIIK
        mod, call_name = get_mod_func(callback)
        # print 'DEBUG MOD %s' % mod
        # print 'DEBUG call_name %s' % call_name
        __import__(mod)
        callback = getattr(sys.modules[mod], call_name)
        self._handlers[cmd] = callback

    def get_handler(self, name):
        return name in self._handlers and self._handlers[name]

    def has_handler(self, name):
        return name in self._handlers
        
    def get_servers(self, name):
        return self._servers.get('quakenet')

class ServerConnection(Thread):
    # TODO ! savoir quand lancer l'autojoin
    _channel_dict = {}
    _events = {}
    _ignores = {}
    
    def __init__(self, bot, id, host='', port=6667, nick='pouhic', identifiant='', realname='',  username='', password='', leaveMsg='', autojoin=[]):
        #super(ServerConnection, self).__init__()
        Thread.__init__(self)
        self.bot = bot
        self.id = id
        self.host = host
        self.port = port
        self.nick = nick
        self.identifiant = identifiant
        self.realname = realname
        self.username = username
        self.password = password
        self.leaveMsg = leaveMsg
        self.autojoin_list = autojoin
        self.authQ = False
        self.modeX = False
        self.serve = True
        self.lastping = int(time.time())

    def set_status(self, serve = True):
        self.serve = serve

    def send_multimsg(self, list_msg):
        for msg in list_msg:
            if msg != None:
                self.send_msg(msg)

    def send_msg(self, msg):
        print "---> %s" % msg
        self.s.send('%s\n' % msg)
        
    def set_nick(self):
        #XXX s'assurer qu'on a bien pris le nom voulu
        self.send_msg("NICK %s" % self.nick)
        
    def set_user(self):
        self.send_msg("USER %s %s foo :%s" % (self.identifiant, self.host, self.realname))

    def say(self, args, place, user=None):
        self.send_msg('PRIVMSG %s :%s' % (place, args))

    def join_chan(self, chan):
        self._channel_dict[chan] = Channel(self, chan)

    def part(self, chan):
        if chan in self._channel_dict:
            self._channel_dict[chan].part()
            del self._channel_dict[chan]
        else:
            #raise un truc ?
            print "je suis pas sur %s" % chan

    def connect(self):
        # commenté pour test offline
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.authQ = False
        self.modeX = False
        tries = 0
        while self.connected == False:
            tries = tries + 1
            self.lastping = int(time.time())
            try:
                self.s.connect((self.host, self.port))
                self.connected = True
            except:
                self.connected = self.reconnect(tries)
        
        self.set_nick()
        self.set_user()

    def reconnect(self, tries):
        print 'WARNING: reconnect()'
        time.sleep(30.0)
        if tries > 10:
            print 'ERROR: nombre maximum d\'essais atteints'
            self.serve = False
            return True
        
        try:
            self.s.connect((self.host, self.port))
            return True
        except:
            return False

    def autojoin(self): 
        for chan in self.autojoin_list:
            self.join_chan(chan)

    def serve_forever(self):
        """ server_forever, or so """
        while self.serve:
            # todo: ping rate average
            if (int(time.time()) - self.lastping) > 600:
                print 'WARNING: timeout'
                self.send_msg('QUIT :%s\n' % self.leaveMsg)
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                offline = True
                while offline:
                    try:
                        print 'WARNING: re-connect()'
                        self.connect()
                        offline = False
                    except:
                        print 'WARNING: loop again'

            self.readbuffer = self.s.recv(1024)
            temp = self.readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                print line
                event = get_event(self, line)
                if event:
                    self.send_multimsg(event.get_response(self))
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

        if self.id == 'quakenet':
            if botnews.active == True:
                botnews.stop()
                print 'DEBUG: en attente de la fin du thread botnews... zuper !'
        print 'DEBUG: END'

    def run(self):
        self.connect()
        self.serve_forever()

class Channel(object):
    _user_list = []

    def __init__(self, server, name=''):
        self.name = name
        self.server = server
        self.send_msg("JOIN %s" % name)
        #XXX fill_user_list

    def send_msg(self, str):
        self.server.send_msg(str)
        

    def part(self):
        self.send_msg("PART %s" % self.name)


data_pattern = re.compile('^((?P<mask>[\w:!~.`^\[\]\-@]+)\ )?(?P<cmd>\w+)\ ((?P<target>#?[\w.\-_]+)\ )?[:+](?P<message>.*)$')

def get_event(connection, data):
    # TODO : faut gere les cas foireux : handler inexistant, et compagnie
    match = data_pattern.match(data)
    if match:
        kw = {}
        for part in ('mask', 'cmd', 'target','message'):
            kw[part] = match.group(part)
        try:
            event = eval('Event%s' % kw['cmd'].capitalize())
            return event(**kw)
        except NameError:
#            print connection.id,
            pass
    else:
        # unknown msg ?
        pass
#        print connection.id, data

class IrcEvent(object):
    def __init__(self, *args, **kwargs):
        super(IrcEvent, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_response(self, server):
        """ this method must return a list of response to send to the server """
        raise NotImplementedError

class EventPing(IrcEvent):
    def get_response(self, server):
        print 'DEBUG ping: %s secondes' % str(int(time.time())-server.lastping)
        server.lastping = int(time.time())
        return ['PONG %s' % self.message]

class EventMode(IrcEvent):
    def get_response(self, server):
        if server.host == 'irc.quakenet.org':
            if server.username == None and server.password == None:
                server.autojoin()
            else:
                if server.authQ == False:
                    server.send_msg("AUTH %s %s" % (server.username, server.password))            
        return []

class EventPrivmsg(IrcEvent):
    def get_response(self, server):
        responses = []

        cmd = self.message.split()[0]
        if cmd[0] == '!' and server.bot.has_handler(cmd[1:]):
            self.cmd = cmd[1:]
            responses.append(server.bot.get_handler(cmd[1:])(server, self)())

        return responses
        
class EventNotice(EventPrivmsg):
    def get_response(self, server):
        if server.host == 'irc.quakenet.org' and not (server.username == None and server.password == None):
            if server.modeX == False and server.authQ == True and self.mask == ':Q!TheQBot@CServe.quakenet.org':
                # lors du 2ème message de :Q!TheQBot@CServe.quakenet.org
                server.send_msg("MODE %s +x" % (server.username))
                server.modeX = True
                server.autojoin()
            
            if self.mask == ':Q!TheQBot@CServe.quakenet.org' and server.authQ == False:
                # lors du 1er message de :Q!TheQBot@CServe.quakenet.org
                server.authQ = True
        return []

class EventAction(IrcEvent):
    def get_response(self, server):
        return []

class Event001(IrcEvent):
    def get_response(self, server):
        if server.host != 'irc.quakenet.org':
            server.autojoin()
        else:
            print '---> QuakeNet, see autojoin later...'
        return []

class EventJoin(IrcEvent):
    def get_response(self, server):
        #server._channel[]
        return []
