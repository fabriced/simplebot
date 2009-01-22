#*-* Coding: UTF-8 *-*

from settings import *
from lib.utils import get_nick

class list(object):

  def __init__(self, main, mask, channel, message):
    self.user = get_nick(mask)
    self.channel = self.user
    self.main = main
    liste = server_dict.keys()
    liste.sort()
    self.main.say('%s' % ', '.join(liste), self.channel )


