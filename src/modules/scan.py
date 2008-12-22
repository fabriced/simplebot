#*-* Coding: UTF-8 *-*

from settings import *
from lib.pyquake3 import *

server_dict = {'pub':'88.191.26.51:27960',
               '1v1':'88.191.26.51:27961',
               'ctf':'88.191.26.51:27962',
               'dm6_1':'88.191.26.51:27963',
               'defrag':'88.191.26.51:27964',
               'dm6_2':'88.191.26.51:27965',
               }


def format_nick(nick):
  """ format players nicknames to remove color infos """
  p = re.compile( '\^.')
  return p.sub('',nick)


def get_nick(host):
  return host.split("!")[0]



class scan(object):
  def __init__(self, main, mask, channel, message):
    self.main = main
    self.user = get_nick(mask)
    self.channel = self.user
    serv = message.split()
    if len(serv) > 1:
      if serv[1] in server_dict.keys():
        self.give_stat(serv[1])
      else:
        self.usage(self.user)
    else:
      self.usage(self.user)




  def usage(self, server):
    self.main.say('usage :', self.user)
    self.main.say(' ', self.user)
    self.main.say(' !scan <serv>', self.user)
    self.main.say(' ', self.user)
    self.main.say(' serv liste : %s' % ", ".join(server_dict.keys()), self.user)




  def give_stat(self, q3server):
    ip = server_dict[q3server]

    q = PyQuake3(ip, rcon_password='')
    q.update()
    self.main.say('%s   %s    map %s    with %s player(s).' %
                          ( q.get_address(),
                          q.vars['sv_hostname'],
                          q.vars['mapname'],
                          len(q.players)),
                          self.channel
                      )
    for player in q.players:
      self.main.say(' %s   %s frags   %s ms\t' % (
                             format_nick(player.name),
                             player.frags,player.ping),
                      self.channel
                      )
