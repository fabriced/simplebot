class part(object):
  def __init__(self, main, mask, channel, message):
    if message.split()[1:]:
      main.s.send("PART %s\n" % message.split()[1])
