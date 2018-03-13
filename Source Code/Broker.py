from socket import *
from threading import Thread
import os
import sys

# Broker.py made by Darling in network
# 1092,1058,1053

SERV_PORT = 50000

#for keep the message of each topic
topicList = {}

#for keep subscriber socket object according to its topic, which is used to send data
clientList = {}

#function for publish message to subscribers according to their topic
def forword(topic):
  try:
    for tempSckt in clientList[topic]: #find each socket that interest in the topic
      try:
        tempSckt.send(topicList[topic].encode('utf-8')) #send data if socket found
      except:
        pass
  except :
    pass
  return

# threaded function for listen to publisher
# when each message from publisher has arrived, do a forward function
# @param s socket object to be treated
def publish_listener(s):
  while True:
    temp = s.recv(1024)
    temp = temp.decode('utf-8')
    text = temp.split(',')
    topic = text[0]
    message = text[1]

    print('Publisher says> '+topic+' : '+message)
    if topic == 'quit':
      print('publisher disconnected')
      break
    elif message=='cancel':
      print('Topic '+topic + ' was canceled')
      topicList.pop(topic) #pop topic data out
    else :
      topicList[topic] = message # add message to topicList
      forword(topic)

# function for handle each connected client (only first time)
# @param s socket object to be treated
def handle_client(s):
    temp = s.recv(1024)
    temp = temp.decode('utf-8')
    text = temp.split(',')
    genre = ''.join(text[0])

    #if it's a publisher, start new thread for listen to it
    if 'P' in genre:
      try:
        Thread(target=publish_listener, args=(s,)).start()
      except:
        print("Cannot start thread..")

    #if it's a subscriber, proceed to keep socket object along with its topic
    if 'S' in genre:
      try:
          clientList[text[1]].append(s)
      except:
        clientList[text[1]] = []
        clientList[text[1]].append(s)
    return

# main function for initialize server
def main():
  addr = ('127.0.0.1', SERV_PORT)
  s = socket(AF_INET, SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print('MQTT Broker started ...')

  while True:
    #passively listen to new connection to be established with this broker
    sckt, addr = s.accept()
    ip, port = str(addr[0]), str(addr[1])
    print('New client connected from ..' + ip + ':' + port)

    handle_client(sckt)


if __name__ == '__main__':
   try:
     main()
   except KeyboardInterrupt:
     print('Interrupted ..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)
