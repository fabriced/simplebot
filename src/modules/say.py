
from lib.decorator import admin_required
from command import command

class say(command):

  @admin_required
  def do(self):
    place, phrase = self.message.split(' ', 1)
    self.main.send('PRIVMSG %s :%s\n' % (place, phrase))
