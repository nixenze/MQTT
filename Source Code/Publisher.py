from socket import * 
import sys

# Publisher.py made by Darling in network
# 1092,1058,1053

MAX_BUF = 2048
SERV_PORT = 50000
topic = ''

#connect to broker via socket with port 50000
addr = ('127.0.0.1', SERV_PORT)
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)

#send message to indicate this client as publisher
Message = 'P'
s.send(Message.encode('utf-8'))

#loop for publish topic and messages
while True:
    print('Published topic name :')
    sys.stdout.flush()
    temp = sys.stdin.readline().strip()
    topic = temp

    #if topic is quit then session is end and send quit session to broker
    if 'quit' in temp:
        print('session end')
        s.send('quit,now'.encode('utf-8'))
        break
    #send message binded with topic to broker
    while True:
        print('Message :')
        sys.stdout.flush()
        temp = sys.stdin.readline().strip()
        Message = topic + ',' + temp
        s.send(Message.encode('utf-8'))
        #if message is 'cancel' it's mean the topic is canceled
        if temp == 'cancel':
            print(topic + ' was canceled')
            break

s.close()

