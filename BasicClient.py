import socket
import threading

headersize = 10 #10 byted
nickname = input("Enter your nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket object
ip = '127.0.0.1' #we are using our own computer for this so this sets the ip to your computer
client.connect((ip, 5554)) 

def recieve():
    while True:
        try:   
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("ERROR")
            client.close()
            break #breaks the loop

def write():
    while True:
        message = '{}: {}'.format(nickname, input(" "))
        client.send(message.encode('utf-8'))
   



recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start() #THIS ALLOWS YOU TO SEND AND RECIVE AT THE SAME TIME

#without threading your program will run one function, one step, one process at a time.
        
    
