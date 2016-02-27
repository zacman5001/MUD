#Without this file running, everyone on the server has to take turns.
#It's kinda cool, but also useless
#BTW I have no idea how to get it to work in realtime without this fake client
import time, random, os, logging, socket, threading, sys
import socket             

def connect():
  host = socket.gethostname() 
  port = 9009
  s = socket.socket()
  s.connect((host, port))
  while True:         
    s.send("null")
    time.sleep(1)

connect()
  
