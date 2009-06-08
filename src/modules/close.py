import sys


from settings import LEAVE_MSG
from command import command

from lib.decorator import admin_required


class close(command):

  @admin_required
  def do(self):
    self.main.send('QUIT %s\n' % LEAVE_MSG)
    self.main.s.close()
    sys.exit(0)
