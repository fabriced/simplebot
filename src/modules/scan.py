#*-* Coding: UTF-8 *-*

from settings import *
from lib.pyquake3 import *

server_dict = {'pub':'88.191.26.51:27960',
               '1v1':'88.191.26.51:27961',
               'ctf':'88.191.26.51:27962',
               'dm6_1':'88.191.26.51:27963',
               'df_1':'88.191.26.51:27964',
               'dm6_2':'88.191.26.51:27965',
               'rox':'88.191.26.51:27966',
               'dm6_3':'88.191.26.51:27967',
               'df_2':'88.191.26.51:27967',
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
    request_list = message.split()[1:]
    if not request_list:
      request_list = server_dict.keys()


    failed = []
    success = True
    for r in request_list:
      if r in server_dict.keys():
        self.give_stat(r)
      else:
        failed.append(r)
        success = False
    if not success:
      self.main.say('echec pour %s' % ','.join(failed), self.channel)




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
    self.main.say('%s -> %s   %s    map %s    with %s player(s).' %
                         (q3server,
                          q.get_address(),
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
