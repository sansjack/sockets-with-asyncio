import asyncio #imports the module asyncio which is in the TPSL ( The Python Standard Libary )
import ast # imports the module abstract syntax tree 

"""
For this example both scripts will be running on the same machine and will be using localhost (127.0.0.1)
This will work fine aslong as we are using the same port for both server and client
"""

print("-- SERVER --") # this is so we know which one is the server console

class Server(asyncio.Protocol):
    def connection_made(self, transport):
        self.address = transport.get_extra_info("peername") #self.address returns a list which has two index IP = [0] and PORT [1]
        self.transport = transport

        self.requests = { "start_connection": self.start_connection } # this is the dict which stores the 
        self.to_client = {} # this is a dict which will store all the data we are going to send to the client

    def connection_lost(self, exception):
        print(f"Connection Lost To {self.address[0]}") 
        if not ( exception == None ):
            print(f"Reason For Disconection: {exception}")
        
    def data_received(self, data):
        try:
            request = ast.literal_eval(data.decode()) # this will raise an expection if the data recived ISNT a python datatype
            assert isinstance(request, dict)
            request = ast.literal_eval(data.decode())
            self.requests[request["start_connection"]](request)
        except Exception as e:
            print(f"An Exception Was Caught: {e}")

    def send_data(self, data):
        self.transport.write(str(data).encode()) # turns data sending into a string then converts it into bytes

    def start_connection(self, data):
        try:
            print(f"Connection Started To {self.address[0]}") 
            self.to_client["A"] = "Hello Client :D" # stores at the key "A" "hello client :D" in the dict which will be sent over the TCP socket
            self.send_data(self.to_client) #finally sending off all of our data
            print(data["some_info"]) # printing the clients hello back message
        except Exception as e:
            print(f"Error In start_connection Function: {e}")

#This is a loop to keep the script running so it can listen out for connections
async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(Server, host, port)
    await server.serve_forever()


#localhost ip = 127.0.0.1 and port 42069 as this port isnt used by any other protocol
asyncio.run(main("127.0.0.1", 42069))