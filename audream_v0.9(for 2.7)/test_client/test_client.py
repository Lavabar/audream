import client as cl
import socket

s = socket.socket()
s.connect(("192.168.31.123",9999))

cl.update_base(s)
  
s.close()
