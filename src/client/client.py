import socket # the client side doesnt use the asyncio module it only needs the socket module which is in The Python Standard Libary
import ast # imports the module abstract syntax tree 

def send_message():
    final_val = "Hello Server!"
    return final_val


starting_requests = {
    "start_connection": "start_connection",
    "some_info" : send_message()

}

print(" -- CLIENT -- ") # this is so we know which one is the client console
class Server:
    # takes the server ip and port
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.sock.connect((self.host_ip, self.host_port))
            self.sock.settimeout(1)
        except:
            pass

    def send_data(self, data):
        self.sock.send(str(data).encode()) #turns string into utf-8

    def close_connection(self): #closes connection
        self.sock.close() 

    def receive_data(self):
        buffer_size = 256
        data = b''
        while True:
            try:
                chunk = self.sock.recv(buffer_size)
            except:
                break
            data += chunk
            if len(chunk) == 0:
                break
        try:
            text_dict = ast.literal_eval(data.decode())
            return text_dict
        except:
            return None

    def is_connected(self): # checks if there is a connection by sending a small packet and if it is sent successfully then return true else return false
        try:
            self.sock.send("".encode())
            return True
        except:
            return False


#sever constructor 
s = Server("127.0.0.1", 42069) #setting the ip and port of the server we are trying to connect to

while True:
    # checking if the try is less than or equal to the amount of times we want to try
    #if it connects successfully 
    if (s.is_connected()):
        s.send_data(starting_requests) # sending our requests which is to call the starting function on the server (the initiation function )
        data = s.receive_data() # getting everything recived an storing it in an varible
        if (data == None):
            print("No Data Recived :(")
            input("") # pauses the connection
        for key, value in data.items():
            print("".join(value)) # printing  the value of everything in the dict which we recived from the server
        input("") # pauses the connection
    else:
        s.close_connection()
        input("Currently Unconnectable :/") #This means the client was refused or the server script is not running
        quit()
else:
    input("Failed to connect you have tried more than 2 times!")
    quit()