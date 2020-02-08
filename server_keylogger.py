import socket
import os
import sys

#**************************************************#
# Func : OpenServer with IP Address and Port
def openserver(host, port):
        if os.path.isfile("log.txt"):
                print "File Exist"
                f=open("buffer.txt", "w+")
        else:
                f=open("buffer.txt", "w")
        server = socket.socket()
        server.bind((host, port))
        server.listen(5)
        print "Listen... " + host + ":" + str(port)
        while True:
                try:
                        client, addr = server.accept()
                        print "Connected by " + addr[0]
                        while True:
                                recv_data = client.recv(1024)
                                packet = recv_data.decode('utf-8')
                                print packet
                                f.write(packet+"\n")
                except KeyboardInterrupt, e:
                        print "\nKeyboardInturrupt!! Quit Process!!"
                        server.close()
                        f.close()
                        sys.exit()

#**************************************************#
if __name__ == "__main__":
        openserver("192.168.0.16", 7000)
