# -*- coding: utf-8 -*-

from settings import ADMINS
from lib.exception import *

def admin_required(func):
  def check_admin(self):
    if self.mask.split('@')[-1] in ADMINS:
      func(self)
    else:
      raise NotAdminError
  return check_admin

# autre decorateur pour faire la meme chose, mais avec un autre nom
devel = admin_required
