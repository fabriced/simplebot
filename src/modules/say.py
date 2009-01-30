# -*- coding:utf-8 -*-


class say(object):
  def __init__(self, main, mask, channel, message):
    if main.is_admin(mask):
      place = message.split()[1]
      phrase = " ".join(message.split()[2:])
      main.send('PRIVMSG %s :%s\n' % (place, phrase))
    else:
      raise NotAdminError
