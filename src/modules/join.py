class join(object):
  def __init__(self, main, mask, channel, message):
    if message.split()[1:]:
      if main.is_admin(host):
        main.s.send("JOIN %s\n" % message.split()[1])
