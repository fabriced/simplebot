# -*- coding: utf-8 -*-
# http://abcdrfc.free.fr/rfc-vf/rfc1459.html#41

import sys
import socket
import string
import time
import imp, inspect

from settings import *


class fafaIrcBot(object):

  def __init__(self):
    self.s=socket.socket()
    self.s.connect((HOST, PORT))
    self.s.send("NICK %s\n" % NICK)
    self.s.send("USER %s %s bla :%s\n" % (IDENT, HOST, REALNAME))
    self.readbuffer=""
    self.canplop = False


  def say(self, args, place, user= None):
    print 'PRIVMSG %s :%s\n' % (place, args)
    self.s.send('PRIVMSG %s :%s\n' % (place, args))


  def send(self, msg):
    self.s.send(msg)


  def auth(self, args, place , user):
    # permet d'acquerir les droits d'admin du bot
    # stock l'host de l'user dans un tableau
    # utiliser des hash md5 sur le passe
    pass

  def bot_auth(self):
    pass
    self.s.send('JOIN #ploooooop.test\n')


  def isAdmin(self, host):
    # return True si l'user est authentifié
    return host.split('@')[-1] in ADMINS


  def getUserNick(self, host):
    return host.split('!')[0][1:]


  def main_loop(self):
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
          if line [1] == 'MODE':
            if line [3] == '+i':
              self.bot_auth()
          if line[1] == "PRIVMSG":
            # generic handler
            if len(line) > 3:
              if len(line[3]) > 1:
                if line[3][1] == '!':
                  methodname = line[3][2:]

                  null, channel, message = string.split(args, ":", 2)
                  mask, null, channel = string.split(string.strip(channel), " ", 2)

                  try:
                    res = imp.find_module(methodname)
                  except:
                    self.s.send("PRIVMSG %s :unknown command : %s\n" % (line[2],
                                                                    methodname))
                  # les "fonctions" dans un répertoire modules
                  msg_type = imp.load_module(methodname, res[0], res[1], res[2])

                  for i in inspect.getmembers(msg_type):
                    if i[0] == methodname:
                      try:
                        i[1](self, mask, channel, message)
                      except:
                        self.s.send("PRIVMSG %s :La commande a echoue : %s\n" % (line[2], methodname))
                        import pdb; pdb.set_trace()


