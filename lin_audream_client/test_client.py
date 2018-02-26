import client as cl
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.31.123",9999))

cl.update_base(s)
  
s.close()
