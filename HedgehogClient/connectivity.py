#!/usr/bin/python3
import socket
import random
import time

class Session:
    Apple = "apple"
    Kit   = "kit"
    Cabbage = "cabbage"
    Clean = "none"
    HOST = 'localhost'
    PORT = 10123
    
    def __init__(self):
        self.debug = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((Session.HOST, Session.PORT))
        data = self.s.recv(1024)
        if data.decode('ascii') != 'HedgeDesk 0.2 protocol.\n':
            print (data)
            raise Exception("Oooops. wrong protocol.")
    def debug(self):
        self.debug = True
    def close(self):
        time.sleep(0.05)
        self.s.send("exit\n".encode());
        self.s.recv(1024)

    def init(self, width, height):
        time.sleep(0.05)
        st = "init "+str(width)+" "+str(height)+"\n"
        self.s.send(st.encode())
        self.s.recv(1024)

    def morph(self,x,y,cell):
        time.sleep(0.05)
        st = "morph "+str(x)+" "+str(y)+" "+cell+"\n"
        self.s.send(st.encode())
        self.s.recv(1024)
    def message(self, message):
        time.sleep(0.05)
        st = "message "+str(message)
        self.s.send(st.encode())
        self.s.recv(1024)

class Hedgehog:
    def __init__(self, session):
        self.session = session
        time.sleep(0.05)
        self.session.s.send("new\n".encode())
        time.sleep(0.05)
        self.session.s.recv(1024)
        time.sleep(0.05)
        self.session.s.send("id\n".encode())
        time.sleep(0.05)
        data = self.session.s.recv(1024)
        self.uid = data.decode('ascii').replace("\n","")
        self.stack = []
        print ("New hedgehog appeared with uid: " + self.uid)
    def move(self, x, y):
        time.sleep(0.05)
        s="move "+str(self.uid)+" "+str(x)+" "+str(y)+"\n"
        print ("Move:"+s)
        self.session.s.send(s.encode())
        self.session.s.recv(1024)
    def take(self):
        time.sleep(0.05)
        s="take "+str(self.uid)+"\n"
        self.session.s.send(s.encode())
        self.session.s.recv(1024)
    def kill(self):
        time.sleep(0.05)
        s="kill "+str(self.uid)+"\n"
        self.session.s.send(s.encode())
        self.session.s.recv(1024)

    def set_power(self,power):
        time.sleep(0.05)
        s="set "+str(self.uid)+" power "+str(power)
        self.session.s.send(s.encode())
        self.session.s.recv(1024)

    def set_health(self,health):
        time.sleep(0.05)
        s="set "+str(self.uid)+" health "+str(health)
        self.session.s.send(s.encode())
        self.session.s.recv(1024)

    def set_name(self,name):
        time.sleep(0.05)
        s="set "+str(self.uid)+" name "+str(name)
        self.session.s.send(s.encode())
        self.session.s.recv(1024)
        
    def set_inventory(self,inv):
        time.sleep(0.05)
        s="set "+str(self.uid)+" inventory "+str(inv)
        self.session.s.send(s.encode())
        self.session.s.recv(1024)
