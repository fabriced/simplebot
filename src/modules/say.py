
from lib.decorator import admin_required
from command import command

class say(command):

    @admin_required
    def __call__(self):
        message = self.message.split(' ', 1)
        if len(message) < 2:
            place = self.user
            phrase = message[0]
            print 'WARNING: manque un argument ?'
        else:
            place = message[0]
            phrase = message[1]
        self.server.send_msg('PRIVMSG %s :%s\n' % (place, phrase))
