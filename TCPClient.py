import socket
import ssl
from socket import *
serverName = '10.197.133.25'
serverPort = 12000
####NEW tls portion
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) #ssl context for client
context.load_verify_locations('server.crt') #load server certificate
##end new tls portion
raw_socket = socket(AF_INET, SOCK_STREAM)#create raw socjket

clientSocket = context.wrap_socket(raw_socket, server_hostname=serverName)#make sure server hostname matches ip in certificate
print("connecting...")
clientSocket.connect((serverName, serverPort)) #TCP connection to server
print("connected!")
#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((serverName, serverPort)) #TCP connection to server

sentence = input('Input sentence:') 
clientSocket.send(sentence.encode())
#wait for response
sentence = clientSocket.recv(1024)
print('From Server:', sentence.decode())
clientSocket.close()
# TCP client program