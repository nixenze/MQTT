from socket import *
from threading import Thread
import os
import sys

# Subscriber.py made by Darling in network
# 1092,1058,1053

MAX_BUF = 2048
SERV_PORT = 50000
username = ''

# threaded function for passively listening to incoming messages
def subscribe(s):
  while True:
    txtin = s.recv(2048)
    txtin = txtin.decode('utf-8')
    print(username+' got message> %s' %txtin)
    sys.stdout.flush()

    if txtin == 'quit':
      print('Client disconnected ...')
      break

# main function fro connecting to broker and send topic
def main():
  addr = ('127.0.0.1', SERV_PORT)
  s = socket(AF_INET, SOCK_STREAM)
  s.connect(addr)

  global username 
  username = input('Enter subscriber name: ')
  topic = input('Place your topic: ')

  s.send(('S,%s'%topic).encode('utf-8'))

  try:
    Thread(target=subscribe, args=(s,)).start()
  except:
    pass



if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted ..')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
