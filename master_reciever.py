#!/usr/bin/env python
import socket


TCP_IP = '127.0.0.1'		# Put here your computer's IP
TCP_PORT = 4005				# Put here the Slave-to-Master Port
BUFFER_SIZE = 1024 # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "Master receive from slave: ", data
    conn.send(data)  # echo
conn.close()
