#!usr/bin/python3

#Realize, the servers job is to manage the connection and services. so messges will not be "broadcasted" to the server rather it will be from the server to all the other clients
#so make sure to try this with mulitple clients!
import socket
import threading

#headersize = 10
ip = '127.0.0.1'
port = 5554
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = ipv4, Sock_Stream = tcp protocol
#basically making a new object, utilizing socket functions and setting the params.
s.bind((ip, port))#bind ip to port
#A socket is an endpoint that sends and recieves data via a port.
s.listen(5) #prepares to listen 

clients = [] #new people connecting to the server go into clients list
nicknames = [] #clients will be prompted to enter a username.

def broadcast(message): #sends message to all clients in server 
	for client in clients: #for every client in the clients array 
		client.send(message) #send them this message

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message) #if message is recived message will be broadcasted
		except:
			index = clients.index(client) #this finds the failed client in the array. (whichever client caused an error)
			clients.remove(client) #removes client from array
			client.close()
			nickname = nicknames[index] #remove the nicknam of the errored client too.
			nickname.remove(nicknames)
			broadcast(f'{nickname} left the room'.encode('utf-8'))
			break #terminates the function and thread.
			


def recieve():
	while True: #while being called
		client, address = s.accept() #here the client socket is accepted and the ip address is passed into the "address" var.
		#msg = input("Enter Message>")#this adds a buffer of 10 characters to your header size
		#msg = f'{len(msg):<{headersize}}' + msg
		print("Connected with {}".format(str(address)))
		client.send('NICK'.encode('utf-8'))
		nickname = client.recv(1024).decode('utf-8') #get nickname from client.. its the first thing sent
		nicknames.append(client) #adds nickname to nicknames array
		clients.append(client) #adds client to client array
		print(f'Nickname of the client is {nickname}!')
		broadcast(f'{nickname} Joined the chat'.encode('utf-8'))
		client.send('Connected to the Server!'.encode('utf-8'))

		#starting a thread because we need to handle each client at the same time we cant just handle them one by one. because what if clients are sending things at the same time? this is inificient

		thread = threading.Thread(target=handle, args=(client,)) #handle the target function
		thread.start() #starts thread. dont use run()

print("Server Online")
recieve()