import sys


from settings import LEAVE_MSG
from lib.exception import *


class close(object):
  def __init__(self, main, mask, channel, message):
    if main.is_admin(mask):
      main.send('QUIT %s\n' % LEAVE_MSG)
      main.s.close()
      sys.exit(0)
    else:
      raise NotAdminError
