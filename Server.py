import sys
import threading
import multiprocessing
import time
import socket
import Settings
from thread import *
import RPi.GPIO as GPIO
from Programs import *
from Animations import *
import json
from neopixel import *
from Driver import *

class SocketServer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while (Settings.INIT_COMPLETE == False): #Waiting Initialized Complete
            time.sleep(1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (Settings.DEBUG == True):
            print ('Socket created')

        try:
            s.bind((Settings.HOST, Settings.PORT))
        except socket.error as msg:
            print ("Bind failed. Error Code : " + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        if (Settings.DEBUG == True):
            print ('Socket bind complete')

        s.listen(10)
        print ('')
        print ('Socket now listening on Port ' + str(Settings.PORT))

        while Settings.EXIT == False:
            conn, addr = s.accept()
            if (Settings.DEBUG == True):
                print ('Connected with ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(clientthread, (conn,))
    def stop(self):
        self.stopped = True

def clientthread(conn):
    try:
        while 1:
            data = conn.recv(1024)
            if not data:
                break

            if data == "":
                print ("You typed zero.\n")
                break
            data = data.replace("\r\n", "")

            parameters = json.loads(data)
            if (Settings.DEBUG == True):
                print (parameters)
            
            if ('cmd' in parameters):
                if(parameters['cmd'] == 'get_data'):
                    replay = 'TOUp='
                    #replay += '&=' + str(Settings) 

                    conn.sendall(replay)

                if(parameters['cmd'] == 'stop'):

                    if(Settings.thread_Programs.is_alive()):
                            Settings.thread_Programs.terminate()
                            time.sleep(0.1)

                    if('animation' in parameters):
                        parameters["data"] = "0-" + Settings.CONFIG.get('Strip', 'LED_COUNT') + ":0"
                        module = __import__('Animations')
                        if(not hasattr(module, parameters['animation'])):
                            conn.sendall('ERROR_PROGRAM_NOT_EXIST')
                            continue
                        method = getattr(module, parameters['animation'])
                        if(hasattr(module, parameters['animation'])):
                            method = getattr(method, parameters['animation'])

                            Settings.thread_Programs = multiprocessing.Process(target=method, args=(parameters, Settings.STRIP))
                            Settings.thread_Programs.daemon = True
                            Settings.thread_Programs.start()
                            Settings.thread_Programs.join()

                    else:
                        if(int(Settings.CONFIG.get('Relai', 'GPIO'))> 0):
                            GPIO.output(int(Settings.CONFIG.get('Relai', 'GPIO')), GPIO.LOW) # 

                        Settings.POWER_STRIP = False
                    conn.sendall('OK')
                if(parameters['cmd'] == 'set'):
                    if(parameters['data'] == ''):
                        conn.sendall('ERROR_NO_DATA')
                        continue

                    if(Settings.thread_Programs.is_alive()):
                            Settings.thread_Programs.terminate()
                            time.sleep(0.1)

                    color = ipsymcon.ReadColorData(str(parameters['data']))

                    if('animation' in parameters): 
                        module = __import__('Animations')
                        if(not hasattr(module, parameters['animation'])):
                            conn.sendall('ERROR_PROGRAM_NOT_EXIST')
                            continue
                        method = getattr(module, parameters['animation'])
                        if(hasattr(module, parameters['animation'])):
                            method = getattr(method, parameters['animation'])

                            Settings.thread_Programs = multiprocessing.Process(target=method, args=(parameters, Settings.STRIP))
                            Settings.thread_Programs.daemon = True
                            Settings.thread_Programs.start()
                    else:
                        if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relai', 'GPIO'))> 0):
                            GPIO.output(int(Settings.CONFIG.get('Relai', 'GPIO')), GPIO.HIGH) # an 
                        Settings.POWER_STRIP = True
                        
                        for key, value in color.iteritems():
                            c = ipsymcon.ColorToRGB(value)
                            Settings.STRIP.setPixelColor(key, Color(c["red"], c["green"], c["blue"]))
                            
                        Settings.STRIP.show()
                    conn.sendall('OK')                         
                if(parameters['cmd'] == 'run'):
                    if(parameters['program'] == ''):
                        conn.sendall('ERROR_PROGRAM_EMPTY')
                        continue
                    module = __import__('Programs')
                    if(not hasattr(module, parameters['program'])):
                        conn.sendall('ERROR_PROGRAM_NOT_EXIST')
                        continue
                    method = getattr(module, parameters['program'])
                    if(hasattr(module, parameters['program'])):
                        method = getattr(method, parameters['program'])
                        if(Settings.thread_Programs.is_alive()):
                            Settings.thread_Programs.terminate()
                        
                        Settings.thread_Programs = multiprocessing.Process(target=method, args=(parameters, Settings.STRIP))
                        Settings.thread_Programs.daemon = True
                        Settings.thread_Programs.start()
                        conn.sendall('OK')
                    else:
                        conn.sendall('ERROR_PROGRAM_NOT_EXIST')
                    
            else:
                conn.sendall('ERROR')
    except:
        print ("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
        pass

def worker(num):
    """thread worker function"""
    print 'Worker:', num
    return