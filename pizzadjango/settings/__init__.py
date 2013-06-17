#-*- coding: utf-8 -*-
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qytst#@ss4k#pq4$61lxmjr1^m3=gzlwn@!8jjfc*ty3&fb6$y'

from .settings import *

try:
    from .settings_local import *
except ImportError, exc:
    print "WARNING: you don't rename settings_local--sample.py to settings_local.py"