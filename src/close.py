import sys

LEAVE_MSG = 'bip'

class close(object):
  def __init__(self, main, mask, channel, message):
    main.send('QUIT %s\n' % LEAVE_MSG)
    main.s.close()
    sys.exit(0)
