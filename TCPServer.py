import socket
import ssl
from socket import *
serverPort = 12000 
serverIP = '' #will listen on all if including current

# --- new tls ---
#create ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#load generated cert and key in same folder
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
# --- NEW TLS SETUP END ---

serverSocket = socket(AF_INET, SOCK_STREAM) #tcp welcome socket creation
serverSocket.bind((serverIP, serverPort)) #bind to address and port
serverSocket.listen(1) #server listens for tcp requests
print('The server is ready to receive')

while True: #infinite loop for server
    #accept tcp connection
    raw_socket, addr = serverSocket.accept() #changed variable name to raw socket from previous
    
    print('Connection from:', addr) #display client address when request is received
    #wrap with tls (handshake)
    try: #try block to handle client communication
        connectionSocket = context.wrap_socket(raw_socket, server_side=True)
    except ssl.SSLError as e:
        print(f"SSL Handshake failed: {e}")
        raw_socket.close()
        continue

    #end updated portion now original from part 1

    try:
        sentence = connectionSocket.recv(1024).decode() #read bytes from socket
        if not sentence: #check for empty message
            print('Client disconnected.') 
        else:#
            connectionSocket.send(sentence.encode())
    except (ConnectionResetError, BrokenPipeError) as e: #handle connection errors, broken pipe is for sending on closed connection
        print(f"An error occurred with {addr}: {e}") #detailed error message
    finally:
        connectionSocket.close() #close connection socket
        print(f"Connection with {addr} closed.")


