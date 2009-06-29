# -*- coding: utf-8 -*-
# http://abcdrfc.free.fr/rfc-vf/rfc1459.html#41

import sys
import socket
import string
import imp, inspect
import glob, os

from settings import *
from lib.exception import *


class fafaIrcBot(object):

  def __init__(self):
    self.s=socket.socket()
    self.s.connect((HOST, PORT))
    self.s.send("NICK %s\n" % NICK)
    self.s.send("USER %s %s bla :%s\n" % (IDENT, HOST, REALNAME))
    self.readbuffer=""
    self.canplop = False
    self.modpath = MODPATH

  def get_modpath(self):
    return self.modpath

  def say(self, args, place, user= None):
    self.s.send('PRIVMSG %s :%s\n' % (place, args))


  def send(self, msg):
    self.s.send(msg)
#    self.s.send("%s\n" % msg)


  def auth(self, args, place , user):
    # permet d'acquerir les droits d'admin du bot
    pass

  def bot_auth(self):
    for channel in CHANNELS:
      self.s.send("JOIN %s\n" % channel)
    pass


  def is_admin(self, host):
    # return True si l'user est authentifié
    return host.split('@')[-1] in ADMINS


  def get_user_nick(self, host):
    return host.split('!')[0]
    
  def recognize_cmd(self, command, path):
    if glob.glob(path + command + '.py'):
      return command
    else:
      for file in glob.glob(path + command[0] + '*.py'):
        if len(command) > len(file)-len(path + '.py')-2 and len(command) < len(file)-len(path + '.py')+2:
          print "current file is: " + file
          return file[len(path):-len('.py')]
    return command


  def main_loop(self):
    self.nb_loop = 0
    while 1:
      if self.nb_loop > 0:
        self.__init__()
      self.nb_loop += 1
      try:
        self.loop()
      except socket.error:
        # rooh, encore floodé
        pass

  def loop(self):
    while 1:
      self.readbuffer = self.s.recv(1024)
      temp = string.split(self.readbuffer, "\n")
      readbuffer = temp.pop()

      for line in temp:
        print line
        args = line
        line = string.rstrip(line)
        line = string.split(line)

        if len(line) > 0:
          if line[0] == "PING":
            self.s.send("PONG %s\n" % line[1])

        if len(line) > 1:
          if line[0] == 'ERROR':
            # ERROR :Closing Link: pouhic by stockholm.se.quakenet.org (Excess Flood)
            self.s.close()
            self.__init__()
          if line [1] == 'MODE':
            if line [3] == '+i':
              self.bot_auth()
          if line[1] == "PRIVMSG":
            # generic handler
            if len(line) > 3:
              if len(line[3]) > 1:
                if line[3][1] == '!':
                  methodname = line[3][2:].replace('!','')
                  if methodname:

                    null, channel, message = string.split(args, ":", 2)
                    mask, null, channel = string.split(string.strip(channel), " ", 2)
                    user = self.get_user_nick(mask)
                    if channel == NICK:
                      channel= self.get_user_nick(mask)
                    # methodname = self.recognize_cmd(methodname, self.modpath)
                    try:
                      res = imp.find_module(methodname, [self.modpath])
                      msg_type = imp.load_module(methodname, res[0], res[1], res[2])
                      for i in inspect.getmembers(msg_type):
                        if i[0] == methodname:
                          try:
                            i[1](self, mask, channel, message)
                          except NotAdminError:
                            self.say("%s: t'as pas le droit\n" % user, user)
                          except:
                            print "Unexpected error:", sys.exc_info()[0]
                            print sys.exc_info()[1]
                            self.s.send("PRIVMSG %s :La commande a echoue : %s\n" % (channel, methodname))
                    except:
                      self.s.send("PRIVMSG %s :unknown command : %s\n" % (self.get_user_nick(mask), methodname))

