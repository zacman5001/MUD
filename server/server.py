#This is mostly franken-code
import sys, time, socket, select, threading, thread
import xml.etree.ElementTree as ET

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9010
socket.setdefaulttimeout(0.1)
userPasswordList = []

ParsingVar = ET.parse("users/database/passwords.xml")
ParsingVar = ParsingVar.getroot()
for string in ParsingVar.findall("string"):
  userPasswordList.append(ParsingVar)

def chat_server():
    playerID = 0
    playerSkillList = []
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while True:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                              
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if "DATATAG_CHATMESSAGE " in data:
                        # there is something in the socket
                        print "T2 - ", data
                        broadcast(server_socket, sock, data)
                    elif "DATATAG_GETSKILLS " in data:
                        data = data.replace("DATATAG_GETSKILLS ","",1)
                        print "Skill check " + data
                        ParsingVar = ET.parse("users/skills/" + data + ".xml")
                        ParsingVar = ParsingVar.getroot()
                        for string in ParsingVar.findall("string"):
                            data2 = "DATATAG_GETSKILLS " + data + " " + string.text
                            playerID = playerID + 1
                        try:
                          returnData(server_socket, sock, data2)
                        except:
                          print "Error returning skill data to user " + data
                    if not data:
                        print "Not Data"
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                    
def returnData (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket == sock :
            try : 
                socket.send(message)
                print "data returned"
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                    print "Connection broken"

 
if __name__ == "__main__":

    sys.exit(chat_server())    
