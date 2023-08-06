from .main import *
from threading import Thread

t = Thread(target=delay_thread)
t.start()