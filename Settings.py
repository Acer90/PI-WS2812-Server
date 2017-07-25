import ConfigParser
from Programs import *
from multiprocessing import Process, Value, Array, Manager
from collections import defaultdict

def init():
    global CONFIG
    CONFIG = ConfigParser.ConfigParser()
    CONFIG.read('Setup.ini')

    global DEBUG, HOST, PORT, INIT_COMPLETE, EXIT, RELAITEST
    DEBUG = False
    INIT_COMPLETE = False
    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = int(CONFIG.get('Server', 'Port'))
    EXIT = False

    global POWER_STRIP, PROGRAM, STRIP, PIXELCOLORDATA
    POWER_STRIP = False
    PROGRAM = ''
    manager = Manager()
    STRIP = ''
    PIXELCOLORDATA = defaultdict(dict)

    global thread_Programs
    thread_Programs = Process()
    thread_Programs.daemon = True